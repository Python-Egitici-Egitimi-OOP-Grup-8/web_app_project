from django.shortcuts import render, redirect  #view function ile return işlemi esnasında kullanılacak fonksiyonlar
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
    sinav = Sinav.objects.get(id=pk)
    if request.method == 'POST':
        sinav.delete()
        return redirect('/')
    context = {'item': sinav}
    return render(request, 'ogretmen/sinavSil.html', context)

def profile(request): #öğretmen profil bölümü viewi
    return render(request, 'ogretmen/profile.html')

def tokenAl(request): #öğretmen token alma bölümü viewi
    return render(request, 'ogretmen/tokenAl.html')

