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

    path('parkingspot/create/', views.createparkingspot, name='createparkingspot'),
    path('parkingspot/', views.viewparkingspot, name='viewparkingspot'),
    path('parkingspot/<int:pk>/', views.viewoneparkingspot, name='viewoneparkingspot'),
    

    path('parkingcategory/create', views.createparkingcategory, name='createparkingcategory'),
    path('parkingcategory/', views.viewparkingcategory, name='viewparkingcategory'),
    path('parkingcategory/<int:pk>/', views.viewoneparkingcategory, name='viewoneparkingcategory'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)