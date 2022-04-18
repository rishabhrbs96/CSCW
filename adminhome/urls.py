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

    path('parkingcategory/create', views.createparkingcategory, name='createparkingcategory'),
    path('parkingcategory/', views.viewparkingcategory, name='viewparkingcategory'),
    path('parkingcategory/<int:pk>/', views.viewoneparkingcategory, name='viewoneparkingcategory'),
    path('parkingcategory/<int:pk>/edit', views.updateparkingcategory, name='updateparkingcategory'),
    path('parkingcategory/<int:pk>/delete', views.deleteparkingcategory, name='deleteparkingcategory'),

    path('upcomingbookings/', views.viewupcomingbookings, name='viewupcomingbookings'),
    path('upcomingbookings/<int:pk>/', views.viewonebooking, name='viewonebooking'),
    path('upcomingbookings/<int:pk>/edit', views.updateupcomingbooking, name='updateupcomingbooking'),
    path('upcomingbookings/<int:pk>/delete', views.deleteupcomingbooking, name='deleteupcomingbooking'),
    path('previousbookings/', views.viewpreviousbookings, name='viewpreviousbookings'),
    path('previousbookings/<int:pk>/', views.viewoneprevbooking, name='viewoneprevbooking'),

    path('userhome/editprofile', views.editprofile, name='editprofile'),
    path('userhome/viewprofile', views.viewprofile, name='viewprofile'),

    path('userhome/addvehicle', views.addvehicle, name='addvehicle'),
    path('userhome/editvehicle', views.editvehicle, name='editvehicle'),
    path('adminhome/verifyvehicle/<int:pk>/', views.verifyvehicle, name='verifyvehicle'),
    path('adminhome/unverifiedvehicles', views.unverifiedvehicles, name='unverifiedvehicles'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)