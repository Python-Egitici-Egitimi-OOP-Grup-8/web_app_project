from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404  # view function ile return işlemi esnasında kullanılacak fonksiyonlar
from oturum.models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
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

def soruKazanim(request,pk):
    sorusay = Sinav.objects.get(id=pk).sorusayisi
    kazanim = SoruKazanim.objects.get(sinav_id=pk)
    form = KazanimSoru(instance=kazanim)
    context = {
        'form':form,
        'say':sorusay
    }
    if request.method == 'POST':
        form = KazanimSoru(request.POST, instance=kazanim)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/kazanimlar.html',context)

def soruPuan(request,pk):
    sorusay = Sinav.objects.get(id=pk).sorusayisi
    puan = SoruPuanlama.objects.get(sinav_id=pk)
    form = SoruPuanForm(instance= puan)
    context = {
        'form':form,
        'say':sorusay
    }
    if request.method == 'POST':
        form = SoruPuanForm(request.POST, instance=puan)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sorupuan.html', context)



def sinavSil(request,pk):
    sinav = Sinav.objects.get(id=pk)
    if request.method == 'POST': #form üzerinden silme onayı gelmişse sil ve sinavlar listesine yönlendir.
        sinav.delete()
        return redirect('/ogretmen/sinavlarim')
    context = {'item': sinav} #link üzerinden gelmişse silme işlemi onayı için yönlendir.
    return render(request, 'ogretmen/sinavSil.html', context)

def profil(request): #öğretmen profil bölümü viewi
    user = User.objects.get(id=request.user.id)
    context = {
        'adi' : user.first_name,
        'soyadi' : user.last_name,
        'email' : user.email,
    }
    # form = Profilim(instance=user)
    # context = {'form': form}
    return render(request, 'ogretmen/profil.html',context)

def updateProfil(request):
    user = User.objects.get(id=request.user.id)
    form = Profilim(instance=user)
    context = {'form': form}
    if request.method == 'POST':
        form = Profilim(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/profilim')
    return render(request, 'ogretmen/profilGuncelle.html', context)

def parolaDegistir(request):
    form = PasswordChangeForm(request.user)
    context = { 'form':form }
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Sistem atmasın diye yeni parola bilgileri ile oturumu güncelleniyor.
            return redirect('/ogretmen/profilim')
    return render(request, 'ogretmen/paroladegistir.html', context)

def sinavEkle(request):
    form = SinavEkle
    context = {'form': form}
    if request.method == 'POST':
        form =SinavEkle(request.POST)
        if form.is_valid():
            sinav = form.save(commit=False)
            sinav.user_id = request.user.id
            sinav.save()
            kazanim = SoruKazanim(sinav_id=sinav.id)
            kazanim.save()
            puan = SoruPuanlama(sinav_id=sinav.id)
            puan.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sinavEkle.html', context)

def cevaplariEkle(request,pk):
    sinav = Sinav.objects.get(id=pk)
    form = CevapEkle(instance=sinav)
    context = {
        'form':form,
        'sorusay':sinav.sorusayisi
    }
    if request.method == 'POST':
        form = CevapEkle(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/dogrucevap.html',context)

def raporAl(request,pk):
    sinav = Sinav.objects.get(id=pk)
    sorupuan = SoruPuanlama.objects.get(sinav_id=sinav.id)
    kazanim = SoruKazanim.objects.get(sinav_id=sinav.id)
    return render(request,'ogretmen/rapor.html')

def tokenAl(request):
    return render(request, 'ogretmen/tokenAl.html')

