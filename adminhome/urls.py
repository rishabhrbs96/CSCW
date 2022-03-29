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
    
    path('edithome/', views.edithome, name='edithome'),
    path('doedit/', views.doedit, name='doedit'),

    path('createparkingspot/', views.createparkingspot, name='createparkingspot'),
    path('docreateparkingspot/', views.docreateparkingspot, name='docreateparkingspot'),
    path('viewparkingspot/', views.viewparkingspot, name='viewparkingspot'),
    path('viewparkingspot/<int:pk>/', views.viewoneparkingspot, name='viewoneparkingspot'),
    

    path('createparkingspotcategory/', views.createparkingspotcategory, name='createparkingspotcategory'),
    path('docreateparkingspotcategory/', views.docreateparkingspotcategory, name='docreateparkingspotcategory'),
    path('viewparkingspotcategory/', views.viewparkingspotcategory, name='viewparkingspotcategory'),
    path('viewparkingspotcategory/<int:pk>/', views.viewoneparkingspotcategory, name='viewoneparkingspotcategory'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)