from django.urls import path
from . import views
from .views import PDFOlustur

urlpatterns = [
    path('',views.ogretmenIndex, name='ogretmen'),
    path('sinavlarim',views.sinavlarim, name='sinavlarim'),
    path('profilim',views.profil, name='profilim'),
    path('raporal/<str:pk>', views.raporAl, name='raporal'),
    path('paroladegis', views.parolaDegistir, name='paroladegis'),
    path('profilguncelle', views.updateProfil, name='profilguncelle'),
    path('pdfal/<str:pk>', PDFOlustur.as_view(), name='pdfal'),
]
