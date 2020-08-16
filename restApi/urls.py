from django.urls import path
from . import views

urlpatterns = [

    #todos
    path('',views.restapideneme),
    path('login',views.login),
    path('signup',views.signup),
    path('ogrencicevapekle',views.OgrenciCevapEkle.as_view()),
]
