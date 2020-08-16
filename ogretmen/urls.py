from django.urls import path
from . import views

urlpatterns = [
    path('',views.ogretmenIndex, name='ogretmen'),
    path('sinavlarim',views.sinavlarim, name='sinavlarim'),
    path('profilim',views.profile, name='profilim'),
    path('token',views.tokenAl, name='tokenAl'),
]
