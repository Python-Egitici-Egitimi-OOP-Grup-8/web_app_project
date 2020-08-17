from django.urls import path
from . import views

urlpatterns = [
    path('',views.ogretmenIndex, name='ogretmen'),
    path('sinavlarim',views.sinavlarim, name='sinavlarim'),
    path('profilim',views.profil, name='profilim'),
    path('token',views.tokenAl, name='tokenAl'),
    path('kazanimlar/<str:pk>', views.kazanimlar, name='kazanimlar'),
    path('sorupuan/<str:pk>', views.soruPuan, name='sorupuan'),
    path('raporal/<str:pk>', views.raporAl, name='raporal'),
    path('sinavsil/<str:pk>', views.sinavSil, name='sinavsil'),
    path('paroladegis', views.parolaDegistir, name='paroladegis'),
    path('profilguncelle', views.updateProfil, name='profilguncelle'),
]
