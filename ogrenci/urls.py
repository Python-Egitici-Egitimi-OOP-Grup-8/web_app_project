from django.urls import path
from . import views
from .views import PDFOlustur

urlpatterns = [
    path('',views.ogrenciIndex, name='ogrhome'),
    path('sinavlarim',views.sinavlarim, name='ogrsinavlarim'),
    path('profilim',views.profil, name='ogrprofilim'),
    path('raporal/<str:pk>', views.raporAl, name='raporal'),
    path('paroladegis', views.parolaDegistir, name='paroladegis'),
    path('profilguncelle', views.updateProfil, name='profilguncelle'),
    path('pdfal/<str:pk>', PDFOlustur.as_view(), name='pdfal'),
]
