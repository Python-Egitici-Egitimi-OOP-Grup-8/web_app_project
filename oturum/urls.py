from django.urls import path
from . import views

urlpatterns = [

    #todos
    path('',views.home),
    path('signup/', views.signupuser, name='signupuser'), 
    path('login/', views.loginuser, name='loginuser'), 
    path('logout/', views.logoutuser, name='logoutuser'),
]
