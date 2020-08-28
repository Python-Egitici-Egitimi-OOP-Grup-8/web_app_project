from django.urls import path
from . import views

urlpatterns = [
    path('',views.ogrenciIndex, name='ogrhome'),
    path('sinavlarim',views.sinavlarim, name='ogrsinavlarim'),
    path('profilim',views.profil, name='ogrprofilim'),
    path('profilguncelle', views.updateProfil, name='ogrprofilguncelle'),
    path('paroladegis', views.parolaDegistir, name='ogrparoladegis'),
    path('raporal/<str:pk>', views.raporAl, name='ogrraporal'),
    path('pdfal/<str:pk>', views.PDFOlustur.as_view(), name='ogrpdfal'),
]
