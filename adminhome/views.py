import json, requests

from django.http import HttpResponseRedirect
from django.core.files import File
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .forms import CreateParkingSpotCategoryForm, HomeForm, CustomUserForm, CustomUserCreationForm
import boto3

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def signout(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('adminhome:index'))
    logout(request)
    return redirect("adminhome:index")

def signin(request):
    if request.method=="POST":
        form = CustomUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("adminhome:edithome")
        else:
            messages.error(request, f"Incorrect credentials! Please try again.")
            return redirect("adminhome:signin")
    form = CustomUserForm
    return render(request=request,
                  template_name="adminhome/signin.html",
                  context = {"form": form})

def signup(request):
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Created New Account: {username}")
            login(request, user)
            messages.info(request, f"you are now logged in as {username}")
            return redirect("adminhome:edithome")
        else:
            messages.error(request, f"Error Signing Up, Please try again")

    form = CustomUserCreationForm
    return render(request=request,
                    template_name="adminhome/signup.html",
                    context={"form": form})


def edithome(request):
    if(not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/edithome.html", {"form": HomeForm(request.POST or None, extra=get_home_metedata())})

def createparkingspotcategory(request):
    if(not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    return render(request, "adminhome/createparkingspotcategory.html", {"form": CreateParkingSpotCategoryForm(request.POST or None)})

def doedit(request):
    if(not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
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
        if(c.startswith('carousel_header')):
            preview_home_metadata['carousel'][int(c.split('_')[-1])]['header'] = request.POST[c]
        if(c.startswith('carousel_body')):
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

def docreatecategory(request):
    if(not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))):
        return HttpResponseRedirect(reverse('adminhome:index'))
    
    new_parking_spot_category = {}
    new_parking_spot_category['name'] = request.POST['name']
    new_parking_spot_category['size'] = request.POST['size']
    new_parking_spot_category['daily_rate'] = request.POST['daily_rate']
    new_parking_spot_category['weekly_rate'] = request.POST['weekly_rate']
    new_parking_spot_category['monthly_rate'] = request.POST['monthly_rate']
    new_parking_spot_category['utility_conversion_rate'] = request.POST['utility_conversion_rate']
    new_parking_spot_category['is_active'] = request.POST['is_active']
    new_parking_spot_category['cancellation_time_window'] = request.POST['cancellation_time_window']
    new_parking_spot_category['cancellation_penalty'] = request.POST['cancellation_penalty']

    return HttpResponseRedirect(reverse('adminhome:createparkingspotcategory'))

def index(request):
    return render(request, "adminhome/index.html", {"metadata":get_home_metedata()})

def get_home_metedata():
    return requests.get('https://d1dmjo0dbygy5s.cloudfront.net/home_metadata.json').json()
