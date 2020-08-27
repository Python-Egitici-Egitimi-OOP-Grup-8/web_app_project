from django.urls import path
from . import views

urlpatterns = [
    path('',views.ogrenciIndex, name='ogrhome'),
    path('sinavlarim',views.sinavlarim, name='ogrsinavlarim'),
    path('profilim',views.profil, name='ogrprofilim'),
    path('profilguncelle', views.updateProfil, name='ogrprofilguncelle'),
    path('paroladegis', views.parolaDegistir, name='ogrparoladegis'),
]
