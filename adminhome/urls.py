from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'adminhome'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    
    path('checkavailability/', views.checkavailability, name='checkavailability'),
    
    path('adminhome/', views.adminhome, name='adminhome'),
    path('userhome/', views.userhome, name='userhome'),

    path('edithome/', views.edithome, name='edithome'),
    path('doedit/', views.doedit, name='doedit'),

    path('parkingspot/create/', views.createparkingspot, name='createparkingspot'),
    path('parkingspot/', views.viewparkingspot, name='viewparkingspot'),
    path('parkingspot/<int:pk>/', views.viewoneparkingspot, name='viewoneparkingspot'),
    path('parkingspot/<int:pk>/edit', views.updateparkingspot, name='updateparkingspot'),
    path('parkingspot/<int:pk>/delete', views.deleteparkingspot, name='deleteparkingspot'),
    path('parkingspot/<int:pk>/showschedule/<str:start_date>/<str:end_date>/', views.showparkingspotschedule, name='showparkingspotschedule'),

    path('parkingcategory/create', views.createparkingcategory, name='createparkingcategory'),
    path('parkingcategory/', views.viewparkingcategory, name='viewparkingcategory'),
    path('parkingcategory/<int:pk>/', views.viewoneparkingcategory, name='viewoneparkingcategory'),
    path('parkingcategory/<int:pk>/edit', views.updateparkingcategory, name='updateparkingcategory'),
    path('parkingcategory/<int:pk>/delete', views.deleteparkingcategory, name='deleteparkingcategory'),

    # path('bookings/', views.userhome),
    path('bookings/create/', views.checkavailability, name='createbooking'),
    path('bookings/<int:bk_id>/', views.viewonebooking, name='viewonebooking'),
    path('bookings/<int:bk_id>/edit/', views.editbooking, name='editbooking'),
    path('bookings/<int:bk_id>/delete/', views.deletebooking, name='deletebooking'),
    path('bookings/<int:bk_id>/confirmcancelbooking/', views.confirmcancelbooking, name='confirmcancelbooking'),
    path('bookings/upcomingbookings/', views.viewupcomingbookings, name='viewupcomingbookings'),
    path('bookings/currentbookings/', views.viewcurrentbookings, name='viewcurrentbookings'),
    path('bookings/previousbookings/', views.viewpreviousbookings, name='viewpreviousbookings'),
    path('bookings/assignslot/', views.assignslottobookings, name='assignslottobookings'),
    path('bookings/assignslot/<int:pk>/', views.assignoneslot, name='assignoneslot'),
    path('bookings/assignslot/<int:pk>/<int:ps>/confirm', views.confirmassignoneslot, name='confirmassignoneslot'),
    path('bookings/<int:bk_id>/addbill', views.addbill, name='addbill'),
    # path('bookings/<int:bk_id>/bills', views.viewallbills, name='viewallbills'),
    path('bookings/<int:bk_id>/bill/<int:bl_id>', views.viewonebill, name='viewonebill'),
    path('bookings/<int:bk_id>/bill/<int:bl_id>/addpayment', views.addpayment, name='addpayment'),
    path('bookings/<int:bk_id>/bill/<int:bl_id>/payonline', views.payonline, name='payonline'),
    
    path('userhome/editprofile', views.editprofile, name='editprofile'),
    path('userhome/changepassword', views.changepassword, name='changepassword'),
    path('userhome/viewprofile', views.viewprofile, name='viewprofile'),
    path('userhome/createaroom', views.createaroom, name='createaroom'),
    path('room/3qRcV', views.room, name='room'),
    path('poll', views.poll, name='poll'),
    path('vote', views.vote, name='vote'),

    path('userhome/addvehicle', views.addvehicle, name='addvehicle'),
    path('userhome/editvehicle/<int:pk>/', views.editvehicle, name='editvehicle'),

    path('bookings/<int:pk>/viewlease', views.viewlease, name='viewlease'),
    path('bookings/<int:pk>/signlease', views.signlease, name='signlease'),

    path('userhome/bookingpickvehicle/<int:parking_category_id>/<str:start_date>/<str:end_date>/', views.booking_pick_vehicle, name='booking_pick_vehicle'),
    path('userhome/bookingconfirmation/<int:vehicle_id>/<int:parking_category_id>/<str:start_date>/<str:end_date>/', views.create_booking, name='create_booking'),
    path('adminhome/verifyvehicle/<int:pk>/', views.verifyvehicle, name='verifyvehicle'),
    path('adminhome/unverifiedvehicles', views.unverifiedvehicles, name='unverifiedvehicles'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)