from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import *

def ogrenciIndex(request):
    return render(request, 'ogrenci/ogrenciIndex.html')

def sinavlarim(request):
    sinavlar = Sinav.objects.filter(user=request.user) #aktif kullanıcıya ait sınav bilgileri sorgulanıyor.
    if sinavlar: #sorgu başarılı ise sinavdolu değeri ile birlikte sözlük oluşturuluyor.
        context = {
            'sinavlar': sinavlar,
            'bosMu': False,
        }
    else:
        context = {
            'sinavlar': sinavlar,
            'bosMu': True,
        }
    return render(request, 'ogrenci/sinavlarim.html', context)

def profil(request):
    user = User.objects.get(id=request.user.id) #profil sayfasında görüntülenecek kullanıcıya bilgiler sorgulanıyor
    context = { #görüntülnecek bilgiler sözlüğe ekleniyor
        'adi' : user.first_name,
        'soyadi' : user.last_name,
        'email' : user.email,
    }
    return render(request, 'ogrenci/profil.html',context)

def updateProfil(request):
    user = User.objects.get(id=request.user.id)
    form = Profilim(instance=user) #user nesnesine ait profilim formunu oluştur.
    context = {'form': form}
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = Profilim(request.POST, instance=user) #user nesnesine ait profilim formunu gelen veri ile oluştur.
        if form.is_valid():
            form.save() #formu kaydet ve veri tabanına işle. commit varsayılan değeri True
            return redirect('/ogrenci/profilim')
    return render(request, 'ogrenci/profilGuncelle.html', context)

def parolaDegistir(request):
    form = PasswordChangeForm(request.user) #Belirtilen kullanıcıya ait parola değiştirme formu örnekleniyor.
    context = { 'form':form }
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = PasswordChangeForm(request.user,request.POST) #elirtilen kullanıcıya ait parola değiştirme formunu yeni gelen veri ile örnekle
        if form.is_valid():
            user = form.save() #formu kaydet ve veri tabanına işle. commit varsayılan değeri True
            update_session_auth_hash(request, user) # Sistem atmasın diye yeni parola bilgileri ile oturumu güncelleniyor.
            return redirect('/ogrenci/profilim')
    return render(request, 'ogrenci/paroladegistir.html', context)