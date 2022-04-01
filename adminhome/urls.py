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
    
    path('adminhome/', views.adminhome, name='adminhome'),

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)