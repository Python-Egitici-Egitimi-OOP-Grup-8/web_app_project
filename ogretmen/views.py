from django.shortcuts import render  #view function ile return edilecek sayfayı render edecek fonksiyon.
from oturum.models import Sinav
from django.http import HttpResponse

def ogretmenIndex(request): #öğretmen ana sayfa viewi
    return render(request, 'ogretmen/ogretmenIndex.html')

def sinavlarim(request): #öğretmen sınavlarım bölümü viewi
    sinavlar = Sinav.objects.filter(user=request.user)
    context = {
        'sinavlar': sinavlar,
    }
    return render(request, 'ogretmen/sinavlarim.html', context)

def kazanimlar(request,pk):
    pass

def soruPuan(request,pk):
    pass

def raporAl(request,pk):
    pass

def sinavSil(request,pk):
    pass

def profile(request): #öğretmen profil bölümü viewi
    return render(request, 'ogretmen/profile.html')

def tokenAl(request): #öğretmen token alma bölümü viewi
    return render(request, 'ogretmen/tokenAl.html')

