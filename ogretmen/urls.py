from django.urls import path
from . import views
from .views import PDFOlustur

urlpatterns = [
    path('',views.ogretmenIndex, name='ogretmen'),
    path('sinavlarim',views.sinavlarim, name='sinavlarim'),
    path('profilim',views.profil, name='profilim'),
    path('token',views.tokenAl, name='tokenAl'),
    path('cevapekle/<str:pk>', views.cevaplariEkle, name='cevapekle'),
    path('kazanimlar/<str:pk>', views.soruKazanim, name='kazanimlar'),
    path('sorupuan/<str:pk>', views.soruPuan, name='sorupuan'),
    path('raporal/<str:pk>', views.raporAl, name='raporal'),
    path('sinavsil/<str:pk>', views.sinavSil, name='sinavsil'),
    path('paroladegis', views.parolaDegistir, name='paroladegis'),
    path('profilguncelle', views.updateProfil, name='profilguncelle'),
    path('sinavekle', views.sinavEkle, name='sinavekle'),
    path('pdfal/<str:pk>', PDFOlustur.as_view(), name='pdfal'),
]
