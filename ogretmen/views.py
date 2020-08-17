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
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sinavEkle.html', context)


def tokenAl(request):
    return render(request, 'ogretmen/tokenAl.html')

