import json, requests, datetime, boto3, math
import random
import time
import pytz

from django.template import context

from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views import View, generic
from django.urls import reverse

from .forms import ParkingCategoryForm, ParkingSpotForm, HomeForm, CustomUserForm, \
    CustomUserCreationForm, VehicleForm, VerifyVehicleForm, CustomUserChangeForm, UserPasswordChangeForm
import boto3

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages

from .models import Booking, ParkingSpot, ParkingCategory, Vehicle, BillDetail, Payment
from .filters import ParkingCatergoryFilter, ParkingSpotFilter, BookingFilter, PreviousAndCurrentBookingFilter
from .forms import BookingForm, ParkingCategoryForm, ParkingSpotForm, HomeForm, CustomUserForm, \
                   CustomUserCreationForm, DateRangeForm, VehicleChangeForm, BillDetailForm, PaymentForm
from .enums import BookingStates, ViewBookings

from datetime import date
from fpdf import FPDF
import string

################################################################################################################
#                                       USER AUTHENTICATION                                                    #
################################################################################################################

def signout(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    logout(request)
    return redirect("adminhome:index")


def signin(request):
    if request.method == "POST":
        form = CustomUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_staff or request.user.is_superuser:
                    return redirect("adminhome:adminhome")
                return redirect("adminhome:userhome")
    else:
        form = CustomUserForm
    return render(request=request,
                  template_name="adminhome/signin.html",
                  context={"form": form})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Created New Account: {username}")
            login(request, user)
            messages.info(request, f"you are now logged in as {username}")
            return redirect("adminhome:index")
    else:
        form = CustomUserCreationForm
    return render(request=request,
                  template_name="adminhome/signup.html",
                  context={"form": form})


################################################################################################################
#                                           PARKING SPOT                                                       #
################################################################################################################

def createparkingspot(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.method == "POST"):
        form = ParkingSpotForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminhome:viewoneparkingspot', args=(form.instance.id,)))
        else:
            return render(request=request,
                          template_name="adminhome/createparkingspot.html",
                          context={"form": form})

    form = ParkingSpotForm
    return render(request=request,
                  template_name="adminhome/createparkingspot.html",
                  context={"form": form})


def viewparkingspot(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    parkingspot_list = ParkingSpotFilter(request.GET, queryset=ParkingSpot.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(parkingspot_list.qs, 2)

    try:
        parkingspot_paginated = paginator.page(page)
    except PageNotAnInteger:
        parkingspot_paginated = paginator.page(1)
    except EmptyPage:
        parkingspot_paginated = paginator.page(paginator.num_pages)
    return render(request, "adminhome/viewparkingspot.html", {'parkingspot_paginated': parkingspot_paginated,
                                                              'filter': parkingspot_list})


def viewoneparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    context = {}
    context["parkingspot"] = ParkingSpot.objects.get(id=pk)
    return render(request, "adminhome/viewoneparkingspot.html", context)


def updateparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    parkingspot = get_object_or_404(ParkingSpot, id=pk)
    form = ParkingSpotForm(request.POST or None, instance=parkingspot)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('adminhome:viewoneparkingspot', args=(form.instance.id,)))

    else:
        return render(request=request,
                      template_name=f"adminhome/updateparkingspot.html",
                      context={"form": form}
                      )


def deleteparkingspot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    parkingspot = get_object_or_404(ParkingSpot, id=pk)
    context["parkingspot"] = parkingspot

    if request.method == 'POST':
        parkingspot.delete()
        return HttpResponseRedirect(reverse("adminhome:viewparkingspot"))

    return render(request, "deleteparkingspot.html", context=context)


################################################################################################################
#                                       PARKING CATEGORY                                                       #
################################################################################################################

def createparkingcategory(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.method == "POST"):
        form = ParkingCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminhome:viewoneparkingcategory', args=(form.instance.id,)))
        else:
            return render(request=request,
                          template_name="adminhome/createparkingcategory.html",
                          context={"form": form})

    form = ParkingCategoryForm
    return render(request=request,
                  template_name="adminhome/createparkingcategory.html",
                  context={"form": form})


def viewparkingcategory(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    parkingcategory_list = ParkingCatergoryFilter(request.GET, queryset=ParkingCategory.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(parkingcategory_list.qs, 2)

    try:
        parkingcategory_paginated = paginator.page(page)
    except PageNotAnInteger:
        parkingcategory_paginated = paginator.page(1)
    except EmptyPage:
        parkingcategory_paginated = paginator.page(paginator.num_pages)
    return render(request, "adminhome/viewparkingcategory.html",
                  {'parkingcategory_paginated': parkingcategory_paginated,
                   'filter': parkingcategory_list})


def viewoneparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    context = {}
    context["parkingcategory"] = ParkingCategory.objects.get(id=pk)
    return render(request, "adminhome/viewoneparkingcategory.html", context)


def updateparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    parkingcategory = get_object_or_404(ParkingCategory, id=pk)
    form = ParkingCategoryForm(request.POST or None, instance=parkingcategory)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('adminhome:viewoneparkingcategory', args=(form.instance.id,)))

    else:
        return render(request=request,
                      template_name=f"adminhome/updateparkingcategory.html",
                      context={"form": form}
                      )


def deleteparkingcategory(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    parkingcategory = get_object_or_404(ParkingCategory, id=pk)
    context["parkingcategory"] = parkingcategory

    if request.method == 'POST':
        parkingcategory.delete()
        return HttpResponseRedirect(reverse("adminhome:viewparkingcategory"))

    return render(request, "deleteparkingcategory.html", context=context)


################################################################################################################
#                                           BOOKINGS                                                           #
################################################################################################################

def viewbookings(request, bookingsType):
    if (not (request.user.is_authenticated)):
        return signin(request)

    if (not (request.user.is_staff or request.user.is_superuser)):
        if (bookingsType == ViewBookings.UPCOMING_BOOKINGS):
            bookings_list = BookingFilter(request.GET, queryset=
            Booking.objects.filter(start_time__gte=datetime.datetime.now(), vehicle_id__user_id=request.user))
        elif (bookingsType == ViewBookings.PREVIOUS_BOOKINGS):
            bookings_list = PreviousAndCurrentBookingFilter(request.GET, queryset=
            Booking.objects.filter(end_time__lte=datetime.datetime.now(), vehicle_id__user_id=request.user))
        else:
            bookings_list = PreviousAndCurrentBookingFilter(request.GET, queryset=
            Booking.objects.filter(start_time__lte=datetime.datetime.now(), end_time__gte=datetime.datetime.now(),
                                   vehicle_id__user_id=request.user))
    else:
        if (bookingsType == ViewBookings.UPCOMING_BOOKINGS):
            bookings_list = BookingFilter(request.GET,
                                          queryset=Booking.objects.filter(start_time__gte=datetime.datetime.now()))
        elif (bookingsType == ViewBookings.PREVIOUS_BOOKINGS):
            bookings_list = PreviousAndCurrentBookingFilter(request.GET, queryset=Booking.objects.filter(
                end_time__lte=datetime.datetime.now()))
        else:
            bookings_list = PreviousAndCurrentBookingFilter(request.GET, queryset=
            Booking.objects.filter(start_time__lte=datetime.datetime.now(), end_time__gte=datetime.datetime.now()))

    # TODO: check the datetime.now() time-zone.
    # print("date: ", datetime.date.today())

    page = request.GET.get('page', 1)
    paginator = Paginator(bookings_list.qs, 2)

    try:
        bookings_paginated = paginator.page(page)
    except PageNotAnInteger:
        bookings_paginated = paginator.page(1)
    except EmptyPage:
        bookings_paginated = paginator.page(paginator.num_pages)

    return render(request, "adminhome/viewbookings.html",
                  {'bookings_paginated': bookings_paginated, 'filter': bookings_list, 'bookingsType': bookingsType})


def viewupcomingbookings(request):
    return viewbookings(request, ViewBookings.UPCOMING_BOOKINGS)


def viewpreviousbookings(request):
    return viewbookings(request, ViewBookings.PREVIOUS_BOOKINGS)


def viewcurrentbookings(request):
    return viewbookings(request, ViewBookings.CURRENT_BOOKINGS)


def create_booking(request, vehicle_id, parking_category_id, start_date, end_date):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    pc = ParkingCategory.objects.get(id=parking_category_id)
    booking = Booking(vehicle_id=vehicle, pc_id=pc, state=BookingStates.NEW, start_time=start_date,
                          end_time=end_date, lease_doc_url='', lease_is_signed_by_user=False, admin_comments='')

    if (request.method == "POST"):
        booking.state = BookingStates.PENDING_LEASE
        booking.last_modified_userid = request.user
        booking.save()
        generatelease(booking.id)
        return HttpResponseRedirect(reverse('adminhome:viewlease', args=(booking.id, )))

    return render(
        request,
        "adminhome/bookingconfirmation.html",
        {'booking': booking}
    )


def assignslottobookings(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    bookings = Booking.objects.filter(state__in=[BookingStates.PENDING_APPROVAL, BookingStates.PENDING_SLOT],start_time__gte=datetime.datetime.now(pytz.timezone('US/Central'))).order_by('lease_sign_time')

    page = request.GET.get('page', 1)
    paginator = Paginator(bookings, 10)

    try:
        bookings_paginated = paginator.page(page)
    except PageNotAnInteger:
        bookings_paginated = paginator.page(1)
    except EmptyPage:
        bookings_paginated = paginator.page(paginator.num_pages)

    return render(request, "adminhome/assignslottobookings.html",
                  {'bookings_paginated': bookings_paginated})


def viewonebooking(request, bk_id):
    if (not (request.user.is_authenticated)):
        return signin(request)

    booking = Booking.objects.get(id=bk_id)
    bills = booking.bills.all()
    unpaid_amount = sum([bl.unpaid_amount for bl in bills])
    
    # NOTE: Logic for admin/user view is handled inside the HTML file.
    context = {"booking": booking, "bills": bills, "unpaid_amount": unpaid_amount}
    return render(request, "adminhome/viewonebooking.html", context)


def editbooking(request, bk_id):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    booking = get_object_or_404(Booking, id=bk_id)
    form = BookingForm(request.POST or None, instance=booking)

    if form.is_valid():
        booking.last_modified_userid = request.user
        form.save()
        return HttpResponseRedirect(reverse('adminhome:viewonebooking', args=(form.instance.id,)))
    else:
        return render(request=request, template_name="adminhome/editbooking.html", context={"form": form})


def deletebooking(request, bk_id):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    booking = get_object_or_404(Booking, id=bk_id)
    context["booking"] = booking

    if request.method == 'POST':
        booking.delete()
        return HttpResponseRedirect(reverse("adminhome:viewupcomingbookings"))

    return render(request, "deletebooking.html", context=context)

def confirmcancelbooking(request, bk_id):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    booking = get_object_or_404(Booking, id=bk_id)
    context["booking"] = booking
    context["error_message"] = ""

    if (booking.state==BookingStates.CANCELED):
        context["error_message"] = "Booking ID#{} has already been canceled.".format(booking.id)
    elif (not (booking.state==BookingStates.APPROVED or booking.state==BookingStates.PAID)):
        context["error_message"] = "Booking ID#{} hasen't been approved yet.".format(booking.id)
    elif (request.method == 'POST'):
        #TODO: Dont execute cancelbooking() for current/previous bookings
        current_time = datetime.datetime.now(pytz.timezone('US/Central'))
        bills = booking.bills.all()
        if len(bills) != 0:
            #TODO: add logic to calculate reservation cost
            refund_amount = sum([bl.paid_amount for bl in bills])
            balance_unpaid_amount = sum([bl.unpaid_amount for bl in bills])
            refund_bill = BillDetail(bill_date=current_time,
                                    reservation_cost=0,
                                    init_meter_reading=0,
                                    utility_cost=0,
                                    paid_amount=(-1)*refund_amount,
                                    unpaid_amount=(-1)*balance_unpaid_amount,
                                    misc_charges=0,
                                    booking_id=booking
                                    )
            refund_bill.save()
        if ((booking.start_time - current_time).days <= booking.pc_id.cancellation_time_window):
            penalty_bill = BillDetail(bill_date=current_time,
                                    reservation_cost=0,
                                    init_meter_reading=0,
                                    utility_cost=0,
                                    paid_amount=0,
                                    unpaid_amount=booking.pc_id.cancellation_penalty,
                                    misc_charges=0,
                                    booking_id=booking
                                    )
            penalty_bill.save()
        booking.state = BookingStates.CANCELED
        booking.parking_spot_id = None
        booking.save()
        return HttpResponseRedirect(reverse("adminhome:viewonebooking", args=(booking.id,)))

    return render(request, "confirmcancelbooking.html", context=context)

def booking_pick_vehicle(request, parking_category_id, start_date, end_date):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:userhome'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))

    # Obtain a list of the user's vehicles.
    vehicles_list = Vehicle.objects.all()
    user_vehicles = []
    for vehicle in vehicles_list:
        if (vehicle.user_id == request.user):
            user_vehicles.append(vehicle)

    return render(request,

                  "adminhome/booking_pick_vehicle.html",
                  {
                      'user_vehicles': user_vehicles,
                      'start_date': start_date,
                      'end_date': end_date,
                      'parking_category_id': parking_category_id,
                  }
                  )


################################################################################################################
#                                               LEASE                                                          #
################################################################################################################

def generatelease(booking_id):
    booking = Booking.objects.get(id=booking_id)
    vehicle = booking.vehicle_id
    parking_category = booking.pc_id
    user = vehicle.user_id

    freq, price = calc_base_rent(booking)

    lease_variables = {
        '<lease_date>': date.today().strftime("%b %d %Y"),
        '<user_name>': str(user.first_name) + " " + str(user.last_name),
        '<parking_spot>': "TBD",
        '<price>': str(price),
        '<lease_frequency>': freq,
        '<start_date>': booking.start_time.strftime("%b %d %Y"),
        '<end_date>': booking.end_time.strftime("%b %d %Y"),
        '<signature>': "",
        '<sign_date>': ""
    }

    # read the sample lease
    f = open("lease_template/sample_lease.txt", "r")
    content = f.read()

    # Change the variable values
    for key, value in lease_variables.items():
        if key in content:
            content = content.replace(key, value)

    # convert it into pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(w=0, h=5, txt=content, border=0, align='1', fill=False)

    # save the file in the s3 aws
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )

    s3 = session.resource('s3')
    key_value = 'lease/{}_{}_lease_{}.pdf'.format(vehicle.user_id, booking_id,
                                                  ''.join(random.choice(string.ascii_lowercase) for i in range(20)))
    s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=key_value,
                                                   Body=pdf.output("{}_{}_lease.pdf".format(vehicle.user_id, booking_id)
                                                                   ,'S').encode('latin-1'),
                                                   ContentType='application/pdf')
    s3_url = 'https://d1dmjo0dbygy5s.cloudfront.net/'
    booking.lease_doc_url = s3_url + key_value
    booking.save()


def generatesignedlease(booking_id):
    booking = Booking.objects.get(id=booking_id)
    vehicle = booking.vehicle_id
    parking_category = booking.pc_id
    user = vehicle.user_id
    lease_sign_time = datetime.datetime.now(pytz.timezone('US/Central'))

    freq, price = calc_base_rent(booking)

    lease_variables = {
        '<lease_date>': date.today().strftime("%b %d %Y"),
        '<user_name>': str(user.first_name) + " " + str(user.last_name),
        '<parking_spot>': "TBD",
        '<price>': str(price),
        '<lease_frequency>': freq,
        '<start_date>': booking.start_time.strftime("%b %d %Y"),
        '<end_date>': booking.end_time.strftime("%b %d %Y"),
        '<signature>': str(user.first_name) + " " + str(user.last_name),
        '<sign_date>': date.today().strftime("%b %d %Y")
    }

    # read the sample lease
    f = open("lease_template/sample_lease.txt", "r")
    content = f.read()

    # Change the variable values
    for key, value in lease_variables.items():
        if key in content:
            content = content.replace(key, value)

    # convert it into pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(w=0, h=5, txt=content, border=0, align='1', fill=False)

    # save the file in the s3 aws
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )

    s3 = session.resource('s3')
    s3_url = 'https://d1dmjo0dbygy5s.cloudfront.net/'

    key_value = booking.lease_doc_url.replace(s3_url,'')
    s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=key_value,
                                                   Body=pdf.output("{}_{}_lease.pdf".format(vehicle.user_id, booking_id)
                                                                   , 'S').encode('latin-1'),
                                                   ContentType='application/pdf')

    # Update booking object
    booking.lease_is_signed_by_user = True
    booking.lease_sign_time = lease_sign_time
    if vehicle.is_verified:
        booking.state = BookingStates.PENDING_SLOT
    else:
        booking.state = BookingStates.PENDING_APPROVAL
    booking.save()


def signlease(request,pk):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))

    booking = get_object_or_404(Booking, id=pk)
    if (booking.lease_is_signed_by_user):
        return HttpResponseRedirect(reverse('adminhome:viewlease', args=(booking.id,)))
    
    generatesignedlease(pk)
    return HttpResponseRedirect(reverse('adminhome:viewlease', args=(booking.id,)))


def viewlease(request, pk):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))

    booking = get_object_or_404(Booking, id=pk)
    if (request.user == booking.vehicle_id.user_id or request.user.is_staff or request.user.is_superuser) and booking.lease_doc_url != '':
        lease_url = booking.lease_doc_url

        return render(
            request,
            "adminhome/viewlease.html",
            {'lease': lease_url,
             'booking': booking}
        )
    else:
        return HttpResponseRedirect(reverse('adminhome:userhome'))


################################################################################################################
#                                       ADMIN HOME                                                             #
################################################################################################################

def adminhome(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/adminhome.html")


def edithome(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/edithome.html",
                  {"form": HomeForm(request.POST or None, extra=get_home_metedata())})


def doedit(request):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    preview_home_metadata = {}
    preview_home_metadata['about'] = {}
    preview_home_metadata['about']['about_header'] = request.POST['about_header']
    preview_home_metadata['about']['about_body'] = request.POST['about_body']

    preview_home_metadata['ameneties'] = {}
    preview_home_metadata['ameneties']['ameneties_header'] = request.POST['ameneties_header']
    preview_home_metadata['ameneties']['ameneties_body'] = request.POST['ameneties_body']

    preview_home_metadata['contact'] = {}
    preview_home_metadata['contact']['phone'] = request.POST['phone']
    preview_home_metadata['contact']['email'] = request.POST['email']
    preview_home_metadata['contact']['location'] = request.POST['location']

    preview_home_metadata['carousel'] = [{} for i in range(3)]
    for i, c in enumerate(request.POST):
        if (c.startswith('carousel_header')):
            preview_home_metadata['carousel'][int(c.split('_')[-1])]['header'] = request.POST[c]
        if (c.startswith('carousel_body')):
            preview_home_metadata['carousel'][int(c.split('_')[-1])]['body'] = request.POST[c]

    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )

    s3 = session.resource('s3')

    sobj = s3.Object(settings.AWS_BUCKET_NAME, settings.AWS_HOME_METADATA_KEY)

    sobj.put(
        Body=(bytes(json.dumps(preview_home_metadata).encode('UTF-8')))
    )

    for i, c in enumerate(request.FILES):
        s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=('media/%s.jpg' % c), Body=request.FILES[c])

    return HttpResponseRedirect(reverse('adminhome:edithome'))


def index(request):
    return render(request, "adminhome/index.html", {"metadata": get_home_metedata()})


def get_home_metedata():
    return requests.get('https://d1dmjo0dbygy5s.cloudfront.net/home_metadata.json').json()


def userhome(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))
    return render(request, "adminhome/userhome.html")


def changepassword(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("adminhome:viewprofile")
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request=request,
                  template_name="adminhome/user_changepassword.html",
                  context={"form": form})


def editprofile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("adminhome:viewprofile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request=request,
                  template_name="adminhome/user_editprofile.html",
                  context={"form": form})


def viewprofile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('adminhome:index'))

    user = request.user
    vehicles = user.vehicle_set.all()

    return render(request, "adminhome/user_viewprofile.html", {'user': user, 'vehicles': vehicles})


def addvehicle(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user_id_id = request.user.id
            vehicle.insurance_doc.name = '{}'.format(vehicle.uuid)
            vehicle.insurance_doc.name = '{}'.format(vehicle.uuid)
            vehicle.save()
            return HttpResponseRedirect(reverse('adminhome:userhome'))
    else:
        form = VehicleForm
    return render(request=request,
                  template_name="adminhome/user_addvehicle.html",
                  context={"form": form})


def unverifiedvehicles(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:index'))

    unverified_vehicles = Vehicle.objects.filter(is_verified=False)
    form = VerifyVehicleForm

    return render(request, "adminhome/admin_view_unverified_vehicles.html",
                  {'unverified_vehicles': unverified_vehicles,
                   'form': form})


def verifyvehicle(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.method == 'POST':
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.is_verified = True
        vehicle.insurance_expiry_date = request.POST['insurance_expiry_date']
        vehicle.save()
    return HttpResponseRedirect(reverse('adminhome:unverifiedvehicles'))


def editvehicle(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('adminhome:index'))

    vehicle = Vehicle.objects.get(pk=pk)

    if not vehicle.user_id_id == request.user.id:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if request.method == 'POST':
        form = VehicleChangeForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.is_verified = False
            vehicle.save()
            return HttpResponseRedirect(reverse('adminhome:viewprofile'))
    else:
        form = VehicleChangeForm(instance=vehicle)
    return render(request, "adminhome/user_editvehicle.html", context={"form": form})


def checkavailability(request):
    parking_categories_all = ParkingCategory.objects.all()
    parking_categories_available = []
    start_date = ''
    end_date = ''
    
    if (request.method == "POST"):
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        form = DateRangeForm(request.POST)
        if form.is_valid():
            form.clean()
            for parking_category in parking_categories_all:
                if(parking_category.is_active):
                    _count = 0
                    for parking_spot in parking_category.parking_spot.all():
                        if(parking_spot.is_active):
                            bookings = parking_spot.booking.exclude(start_time__date__gte=request.POST['end_date'],).exclude(end_time__date__lt=request.POST['start_date'],)
                            if(not bookings.exists()):
                                _count = _count + 1
                    if(_count > 0):
                        parking_categories_available.append(parking_category)
    else:
        form = DateRangeForm
    return render(
        request,
        "adminhome/checkavailability.html",
        {
            'parking_categories_available': parking_categories_available,
            'form': form,
            'start_date': start_date,
            'end_date': end_date,
        }
    )


def showparkingspotschedule(request, pk, start_date, end_date):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    start_time = datetime.datetime.combine(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                           datetime.datetime.min.time())
    end_time = datetime.datetime.combine(datetime.datetime.strptime(end_date, '%Y-%m-%d'), datetime.datetime.min.time())
    twd = (end_time - start_time).days

    pc = []
    parking_spot = ParkingSpot.objects.get(id=pk)

    if (parking_spot.is_active):
        pc.append([parking_spot, [0, []]])
        bookings = parking_spot.booking.filter(start_time__lte=end_time, ).filter(end_time__gte=start_time, ).order_by(
            'start_time', 'end_time')
        len_bookings = len(bookings)
        if (len_bookings == 0):
            pc[-1][1][1].append([False, 100, ""])
            pc[-1][1][0] = 100
        else:
            bookings[0].start_time = bookings[0].start_time.replace(tzinfo=None)
            bookings[0].end_time = bookings[0].end_time.replace(tzinfo=None)
            if (bookings[0].start_time > start_time):
                wd = bookings[0].start_time - start_time
                pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                pc[-1][1][0] += (100 * wd.days) / twd
            i = 0
            for booking in bookings:
                booking.start_time = booking.start_time.replace(tzinfo=None)
                booking.end_time = booking.end_time.replace(tzinfo=None)
                s = max(booking.start_time, start_time)
                e = min(booking.end_time, end_time)
                wd = e - s
                pc[-1][1][1].append([True, (100 * wd.days) / twd, booking])
                i = i + 1
                if (i < len_bookings):
                    bookings[i].start_time = bookings[i].start_time.replace(tzinfo=None)
                    bookings[i].end_time = bookings[i].end_time.replace(tzinfo=None)
                    s = max(booking.start_time, start_time)
                    wd = bookings[i].start_time - e
                    pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                    pc[-1][1][0] += (100 * wd.days) / twd
            if (bookings[len_bookings - 1].end_time < end_time):
                wd = end_time - bookings[len_bookings - 1].end_time
                pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                pc[-1][1][0] += (100 * wd.days) / twd

    pc.sort(reverse=True, key=lambda x: x[1][0])

    return render(request,
                  "adminhome/showparkingspotschedule.html",
                  {
                      'start_date': start_date,
                      'end_date': end_date,
                      'parking_spot': parking_spot,
                      'pc': pc
                  }
                  )


def confirmassignoneslot(request, pk, ps):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    context = {}
    booking = Booking.objects.get(id=pk)
    parking_spot = ParkingSpot.objects.get(id=ps)
    context["booking"] = booking
    context["parking_spot"] = parking_spot
    context["error_message"] = ""
    
    if (not (parking_spot.is_active and parking_spot.parking_category_id.is_active)):
        context["error_message"] = "Parking Spot {} is inactive.".format(parking_spot)
    elif (len(parking_spot.booking.filter(start_time__lte=booking.end_time, ).filter(end_time__gte=booking.start_time, )) != 0):
        context["error_message"] = "Parking Spot {} is not completely avialable from {} to {}.".format(parking_spot, booking.start_time.date(), booking.end_time.date())
    elif request.method == 'POST':
        is_reassignnment = False
        if booking.parking_spot_id:
            is_reassignnment = True
        booking.parking_spot_id = parking_spot
        booking.state = BookingStates.APPROVED
        #TODO: add logic to calculate reservation cost
        reservation_cost = ((booking.end_time - booking.start_time).days)*booking.pc_id.daily_rate
        if not is_reassignnment:
            base_bill = BillDetail(bill_date=datetime.datetime.now(pytz.timezone('US/Central')),
                                    reservation_cost=reservation_cost,
                                    init_meter_reading=0,
                                    utility_cost=0,
                                    paid_amount=0,
                                    unpaid_amount=reservation_cost,
                                    misc_charges=0,
                                    booking_id=booking
                                    )
            base_bill.save()
        booking.save()
        return HttpResponseRedirect(reverse("adminhome:viewonebooking", args=(booking.id,)))

    return render(request, "confirmassignoneslot.html", context=context)


def assignoneslot(request, pk):
    if (not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))

    current_booking = Booking.objects.get(id=pk)
    twd = (current_booking.end_time - current_booking.start_time).days

    form = VerifyVehicleForm

    if request.method == 'POST':
        vehicle = Vehicle.objects.get(pk=current_booking.vehicle_id.id)
        vehicle.is_verified = True
        vehicle.insurance_expiry_date = request.POST['insurance_expiry_date']
        vehicle.save()
        current_booking.state = BookingStates.PENDING_SLOT

    pc = []
    current_booking_slot = []
    for parking_spot in current_booking.pc_id.parking_spot.all():
        if (parking_spot.is_active):
            pc.append([parking_spot, [0, []]])
            bookings = parking_spot.booking.filter(start_time__lte=current_booking.end_time, ).filter(
                end_time__gte=current_booking.start_time, ).order_by('start_time', 'end_time')
            len_bookings = len(bookings)
            if (len_bookings == 0):
                pc[-1][1][1].append([False, 100, ""])
                pc[-1][1][0] = 100
                continue
            if (bookings[0].start_time > current_booking.start_time):
                wd = bookings[0].start_time - current_booking.start_time
                pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                pc[-1][1][0] += (100 * wd.days) / twd
            i = 0
            for booking in bookings:
                s = max(booking.start_time, current_booking.start_time)
                e = min(booking.end_time, current_booking.end_time)
                wd = e - s
                pc[-1][1][1].append([True, (100 * wd.days) / twd, booking])
                i = i + 1
                if (i < len_bookings):
                    wd = bookings[i].start_time - e
                    pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                    pc[-1][1][0] += (100 * wd.days) / twd
            if (bookings[len_bookings - 1].end_time < current_booking.end_time):
                wd = current_booking.end_time - bookings[len_bookings - 1].end_time
                pc[-1][1][1].append([False, (100 * wd.days) / twd, ""])
                pc[-1][1][0] += (100 * wd.days) / twd
            
            if (current_booking.parking_spot_id and parking_spot.id == current_booking.parking_spot_id.id):
                current_booking_slot = pc[-1][1][1]

    pc.sort(reverse=True, key=lambda x: x[1][0])

    return render(request,"adminhome/assignoneslot.html",{'current_booking': current_booking,'pc': pc,'form': form, 'current_booking_slot': current_booking_slot})


def addbill(request, bk_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:userhome'))

    if request.method == "POST":
        form = BillDetailForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.bill_date = datetime.datetime.now(pytz.timezone('US/Central'))
            bill.booking_id_id = bk_id
            bill.meter_rate = ParkingCategory.objects.get(pk=request.GET.get('pc')).utility_conversion_rate
            bill.utility_cost = (bill.end_meter_reading - bill.init_meter_reading) * bill.meter_rate
            bill.save()
            return HttpResponseRedirect(reverse('adminhome:viewonebooking', args=(bk_id,)))
    else:
        form = BillDetailForm()
    return render(request=request,
                  template_name="adminhome/admin_add_bill.html",
                  context={"form": form})


def viewonebill(request, bk_id, bl_id):
    if (not (request.user.is_authenticated)):
        return signin(request)

    context = {"bill": BillDetail.objects.get(id=bl_id), "payments": Payment.objects.filter(bill_id=bl_id)}
    return render(request, "adminhome/viewonebill.html", context)


def addpayment(request, bk_id, bl_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:userhome'))

    if request.method == "POST":
        form = PaymentForm(request.POST)
        print(form)
        if form.is_valid():
            payment = form.save(commit=False)
            bill = BillDetail.objects.get(id=bl_id)
            if bill.unpaid_amount < payment.amount:
                form.add_error('amount', "Payment amount can't be greater than bill's unpaid amount ${}".format(bill.unpaid_amount))
                return render(request=request,
                  template_name="adminhome/admin_add_payment.html",
                  context={"form": form})
            bill.unpaid_amount = bill.unpaid_amount - payment.amount
            bill.paid_amount = payment.amount
            bill.save()
            payment.time = datetime.datetime.now(pytz.timezone('US/Central'))
            payment.bill = bill
            payment.save()
            return HttpResponseRedirect(reverse('adminhome:viewonebill', args=(bk_id, bl_id,)))
    else:
        form = PaymentForm()
    return render(request=request,
                  template_name="adminhome/admin_add_payment.html",
                  context={"form": form})

def payonline(request, bk_id, bl_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminhome:index'))

    if (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect(reverse('adminhome:adminhome'))

    bill = BillDetail.objects.get(id=bl_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        print(form)
        if form.is_valid():
            payment = form.save(commit=False)
            bill = BillDetail.objects.get(id=bl_id)
            if bill.unpaid_amount < payment.amount:
                form.add_error('amount', "Payment amount can't be greater than bill's unpaid amount ${}".format(bill.unpaid_amount))
                return render(request=request,
                  template_name="adminhome/admin_add_payment.html",
                  context={"form": form})
            bill.unpaid_amount = bill.unpaid_amount - payment.amount
            if bill.unpaid_amount == 0:
                booking = bill.booking_id
                booking.state = BookingStates.PAID
                booking.save()
            bill.save()
            payment.time = datetime.datetime.now(pytz.timezone('US/Central'))
            payment.bill = bill
            payment.save()
            return HttpResponseRedirect(reverse('adminhome:viewonebill', args=(bk_id, bl_id,)))
    else:
        form = PaymentForm()
    return render(request=request,
                  template_name="adminhome/user_payonline.html",
                  context={"bill": bill, "unpaid_amount_integral": int(math.modf(bill.unpaid_amount)[1]), "unpaid_amount_decimal": int(100*math.modf(bill.unpaid_amount)[0])})

def calc_base_rent(booking):
    parking_category = booking.pc_id
    lease_duration = (booking.end_time - booking.start_time).days

    if 7 <= lease_duration <= 30:
        freq = 'Week'
        price = parking_category.weekly_rate
    elif lease_duration < 7:
        freq = 'Day'
        price = parking_category.daily_rate
    else:
        freq = 'Month'
        price = parking_category.monthly_rate

    return freq, price
