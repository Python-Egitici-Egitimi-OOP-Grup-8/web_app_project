from django.shortcuts import render, redirect, get_object_or_404  # view function ile return işlemi esnasında kullanılacak fonksiyonlar
from oturum.models import *
from .forms import *
from django.http import HttpResponse

def ogretmenIndex(request): #öğretmen ana sayfa viewi
    return render(request, 'ogretmen/ogretmenIndex.html')

def sinavlarim(request): #öğretmen sınavlarım bölümü viewi
    sinavlar = Sinav.objects.filter(user=request.user)
    if sinavlar:
        context = {
            'sinavlar': sinavlar,
            'bosMu': False,
        }
    else:
        context = {
            'sinavlar': sinavlar,
            'bosMu': True,
        }
    return render(request, 'ogretmen/sinavlarim.html', context)

def kazanimlar(request,pk):
    kazanim = SoruKazanim.objects.get(sinav_id=pk)
    form = KazanimSoru(instance=kazanim)
    context = {'form': form}
    if request.method == 'POST':
        form = KazanimSoru(request.POST, instance=kazanim)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/kazanimlar.html',context)

def soruPuan(request,pk):
    puan = SoruPuanlama.objects.get(sinav_id=pk)
    form = SoruPuanForm(instance= puan)
    context = {'form': form}
    if request.method == 'POST':
        form = SoruPuanForm(request.POST, instance=puan)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sorupuan.html', context)

def raporAl(request,pk):
    pass

def sinavSil(request,pk):
    sinav = Sinav.objects.get(id=pk)
    if request.method == 'POST': #form üzerinden silme onayı gelmişse sil ve sinavlar listesine yönlendir.
        sinav.delete()
        return redirect('/ogretmen/sinavlarim')
    context = {'item': sinav} #link üzerinden gelmişse silme işlemi onayı için yönlendir.
    return render(request, 'ogretmen/sinavSil.html', context)

def profile(request): #öğretmen profil bölümü viewi
    user = User.objects.get(id=request.user.id)
    context = {
        'adi' : user.first_name,
        'soyadi' : user.last_name,
        'email' : user.email,
    }
    # form = Profilim(instance=user)
    # context = {'form': form}
    return render(request, 'ogretmen/profile.html',context)

def updateProfile(request):
    pass

def parolaDegistir(request):
    pass

def tokenAl(request): #öğretmen token alma bölümü viewi
    return render(request, 'ogretmen/tokenAl.html')

