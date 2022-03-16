from django.urls import path

from . import views

app_name = 'adminhome'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    
    path('edithome/', views.edithome, name='edithome'),
    path('doedit/', views.doedit, name='doedit'),
]