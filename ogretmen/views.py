from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from oturum.models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import numpy as np

def ogretmenIndex(request):
    return render(request, 'ogretmen/ogretmenIndex.html')

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
    return render(request, 'ogretmen/sinavlarim.html', context)

def soruKazanim(request,pk):
    sinav = Sinav.objects.get(id=pk)
    kazanim = SoruKazanim.objects.get(sinav_id=pk)
    form = KazanimSoru(instance=kazanim)
    context = {
        'form': form,
        'say': sinav.sorusayisi
    }
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = KazanimSoru(request.POST, instance=kazanim)
        if form.is_valid():
            form.save()
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/kazanimlar.html',context)

def soruPuan(request,pk):
    sorusay = Sinav.objects.get(id=pk).sorusayisi
    puan = SoruPuanlama.objects.get(sinav_id=pk) #Seçilen sınava ait puan değerleri getiriliyor.
    form = SoruPuanForm(instance = puan) #Kullanıcıya görüntülenmek üzere puan değerleri ile form örneği oluşturuluyor.
    context = {
        'form':form,
        'say':sorusay
    }
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = SoruPuanForm(request.POST, instance=puan) #Formdan gelen soru puanları işlenmek üzere SoruPuanForm örneği oluşturuluyor.
        if form.is_valid():
            form.save() #yeni puan değerleri işleniyor.
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sorupuan.html', context)

def sinavSil(request,pk):
    sinav = Sinav.objects.get(id=pk)
    if request.method == 'POST': #form üzerinden silme onayı gelmişse sil ve sinavlar listesine yönlendir.
        sinav.delete()
        return redirect('/ogretmen/sinavlarim')
    context = {'item': sinav} #link üzerinden gelmişse silme işlemi onayı için yönlendir.
    return render(request, 'ogretmen/sinavSil.html', context)

def profil(request):
    user = User.objects.get(id=request.user.id) #profil sayfasında görüntülenecek kullanıcıya bilgiler sorgulanıyor
    context = { #görüntülnecek bilgiler sözlüğe ekleniyor
        'adi' : user.first_name,
        'soyadi' : user.last_name,
        'email' : user.email,
    }
    return render(request, 'ogretmen/profil.html',context)

def updateProfil(request):
    user = User.objects.get(id=request.user.id)
    form = Profilim(instance=user) #user nesnesine ait profilim formunu oluştur.
    context = {'form': form}
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = Profilim(request.POST, instance=user) #user nesnesine ait profilim formunu gelen veri ile oluştur.
        if form.is_valid():
            form.save() #formu kaydet ve veri tabanına işle. commit varsayılan değeri True
            return redirect('/ogretmen/profilim')
    return render(request, 'ogretmen/profilGuncelle.html', context)

def parolaDegistir(request):
    form = PasswordChangeForm(request.user) #Belirtilen kullanıcıya ait parola değiştirme formu örnekleniyor.
    context = { 'form':form }
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = PasswordChangeForm(request.user,request.POST) #elirtilen kullanıcıya ait parola değiştirme formunu yeni gelen veri ile örnekle
        if form.is_valid():
            user = form.save() #formu kaydet ve veri tabanına işle. commit varsayılan değeri True
            update_session_auth_hash(request, user) # Sistem atmasın diye yeni parola bilgileri ile oturumu güncelleniyor.
            return redirect('/ogretmen/profilim')
    return render(request, 'ogretmen/paroladegistir.html', context)

def sinavEkle(request):
    form = SinavEkle  # SinavEkle django formunu örnekle
    context = {'form': form} #template e gönderilmek üzere sözlüğe ekle.
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form =SinavEkle(request.POST)
        if form.is_valid():
            sinav = form.save(commit=False) # formu kaydet fakat veri tabanına işleme.Bazı alanları düzenlemek üsere beklet.
            sinav.user_id = request.user.id #userid alanını şu anki kullanıcı id si olarak ayarla.
            sinav.save() #formu kaydet ve veri tabanına işle. commit varsayılan değeri True
            kazanim = SoruKazanim(sinav_id=sinav.id) #SoruKazanim modelinde belirtilen sınava ait boş kayıt oluştur.
            kazanim.save() #işle
            puan = SoruPuanlama(sinav_id=sinav.id) #SoruPuanlama modelinde belirtilen sınava ait boş kayıt oluştur.
            puan.save() #işle
            return redirect('/ogretmen/sinavlarim')
    return render(request, 'ogretmen/sinavEkle.html', context)

def cevaplariEkle(request,pk):
    sinav = Sinav.objects.get(id=pk) #seçilen id değerine sahip sınav bilgileri getiriliyor.
    form = CevapEkle(instance=sinav) #üzerinde işlem yapılacak sınav örneği için doğru cevap ekleme/değiştirme formu oluşturuluyor. Varsa değerler getiriliyor.
    context = {
        'form': form,
        'sorusay': sinav.sorusayisi,
    }
    if request.method == 'POST': #sayfaya form üzerinden gelinmişse.
        form = CevapEkle(request.POST,instance=sinav) #yeni doğru cevap değerleri ile birlikte işlenmek üzere form oluşturuluyor.
        if form.is_valid():
            form.save(commit=True) #veri tabanına işleniyor.
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/dogrucevap.html',context)

def raporAl(request,pk):
    sorusayisi = Sinav.objects.get(id=pk).sorusayisi
    sinav = Sinav.objects.filter(id=pk).values()
    ogrcevaplar = OgrenciCevap.objects.filter(sinav_id=pk).values()
    sorupuan = SoruPuanlama.objects.filter(sinav_id=pk).values()
    raporList = []
    rapor = [0,'cevap','anahtarı']
    cevaplist=[]

    for dcevap in sinav:
        say = 1
        while say <= sorusayisi:
            rapor.append(dcevap[f'C{say}_id'])
            cevaplist.append(dcevap[f'C{say}_id'])
            say += 1
        rapor.append(sorusayisi)
        rapor.append(100)
    raporList.append(rapor) # ilk satır olarak doğru cevaplar belirlenen id ile ekleniyor.

    puanlist=[]
    for puan in sorupuan:
        say=1
        while say<=sorusayisi:
            puanlist.append(puan[f'P{say}'])
            say += 1
    # print(puanlist)

    for ogr in ogrcevaplar:
        puan = 0
        dogru_sayisi = 0
        ogrenci = User.objects.get(id=ogr['ogrenci_id'])
        rapor = [ogrenci.id, ogrenci.first_name, ogrenci.last_name]
        say=1
        while say<=sorusayisi:
            rapor.append(ogr[f'C{say}_id'])
            if ogr[f'C{say}_id'] == cevaplist[say-1]:
                dogru_sayisi += 1
                puan += puanlist[say-1]
            say += 1
        rapor.append(dogru_sayisi)
        rapor.append(puan)
        raporList.append(rapor)
    raporList = np.array(raporList)
    # print(raporList)
    context={
        'rapor':raporList
    }
    kazanim = SoruKazanim.objects.get(sinav_id=pk)
    return render(request,'ogretmen/rapor.html',context)

def tokenAl(request):
    token, created = Token.objects.get_or_create(user_id=request.user.id) #varsa getir yoksa yeni token oluştur.
    context = {'anahtar':token}
    return render(request, 'ogretmen/tokenAl.html',context)

