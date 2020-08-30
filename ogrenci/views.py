import numpy as np
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View

from ogretmen.utilities import render_to_pdf
from .forms import *

def ogrenciIndex(request):
    return render(request, 'ogrenci/ogrenciIndex.html')

def sinavlarim(request):
    icerik = OgrenciCevap.objects.filter(ogrenci_id=request.user.id)
    if icerik:
        context = {
            'icerik': icerik,
            'bosMu': False,
        }
    else:
        context = {
            'icerik': icerik,
            'bosMu': True,
        }
    return render(request, 'ogrenci/sinavlarim.html', context)

def profil(request):
    user = User.objects.get(id=request.user.id) #profil sayfasında görüntülenecek kullanıcıya bilgiler sorgulanıyor
    context = { #görüntülnecek bilgiler sözlüğe ekleniyor
        'adi' : user.first_name,
        'soyadi' : user.last_name,
        'email' : user.email,
        'id' : user.id,
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

def raporAl(request, pk):
    try:
        sorusayisi = Sinav.objects.get(id=pk).sorusayisi
        sinav = Sinav.objects.filter(id=pk).values()
        ogrenciler = OgrenciCevap.objects.filter(sinav_id=pk)
        ogrcevaplar = ogrenciler.values()
        sorupuan = SoruPuanlama.objects.filter(sinav_id=pk).values()
        raporList = []
        cevap_kagidi = [0,'Cevap','Anahtarı']
        cevaplist=[]

        for dcevap in sinav:
            say = 1
            while say <= sorusayisi:
                if dcevap[f'C{say}_id']==1:
                    cevap_kagidi.append('A')
                elif dcevap[f'C{say}_id']==2:
                    cevap_kagidi.append('B')
                elif dcevap[f'C{say}_id']==3:
                    cevap_kagidi.append('C')
                elif dcevap[f'C{say}_id'] == 4:
                    cevap_kagidi.append('D')
                elif dcevap[f'C{say}_id'] == 5:
                    cevap_kagidi.append('E')
                else:
                    cevap_kagidi.append('girilmemiş')
                cevaplist.append(dcevap[f'C{say}_id'])
                say += 1
            cevap_kagidi.append(sorusayisi)
            cevap_kagidi.append(0)
            cevap_kagidi.append(100)

        puanlist=[]
        for puan in sorupuan:
            say=1
            while say <= sorusayisi:
                puanlist.append(puan[f'P{say}'])
                say += 1

        for ogr in ogrcevaplar:
            puan = 0
            dogru_sayisi = 0
            yanlis_sayisi = 0
            ogrenci = User.objects.get(id=ogr['ogrenci_id'])
            rapor = [ogrenci.id, ogrenci.first_name, ogrenci.last_name]
            say=1
            while say<=sorusayisi:
                if ogr[f'C{say}_id'] is None:
                    rapor.append(0)
                else:
                    rapor.append(ogr[f'C{say}_id'])
                    if ogr[f'C{say}_id'] == cevaplist[say-1]:
                        dogru_sayisi += 1
                        puan += puanlist[say - 1]
                    else:
                        yanlis_sayisi += 1
                say += 1
            rapor.append(dogru_sayisi)
            rapor.append(yanlis_sayisi)
            rapor.append(puan)
            if(ogrenci.id==request.user.id):
                ogrenci_cevap = rapor.copy()
            raporList.append(rapor)
        raporList = np.array(raporList)
        x = np.array(raporList[:, -1]).astype(np.int32)
    except Exception as e:
        return render(request,'ogrenci/rapor.html', {'hata':True})
    context={
        'cevap_kagidi': cevap_kagidi,
        'ogr_cevaplari': ogrenci_cevap,
        'ogr_puan': ogrenci_cevap[-1],
        'yanlis_say': ogrenci_cevap[-2],
        'dogru_say': ogrenci_cevap[-3],
        'sorusayilist': range(1,sorusayisi+1),
        'sorusayisi':sorusayisi+3,
        'max_not': x.max(),
        'min_not': x.min(),
        'ortalama': round(np.average(x),1),
        'sinav_adi':Sinav.objects.get(id=pk).baslik,
        'sinav_id': pk,
    }
    return render(request,'ogrenci/rapor.html',context)

class PDFOlustur(View):
    def get(self, request, pk, *args, **kwargs):
        template = get_template('ogretmen/pdf/rapor_pdf.html')
        try:
            sorusayisi = Sinav.objects.get(id=pk).sorusayisi
            sinav = Sinav.objects.filter(id=pk).values()
            ogrenciler = OgrenciCevap.objects.filter(sinav_id=pk)
            ogrcevaplar = ogrenciler.values()
            sorupuan = SoruPuanlama.objects.filter(sinav_id=pk).values()
            raporList = []
            cevap_kagidi = [0, 'Cevap', 'Anahtarı']
            cevaplist = []

            for dcevap in sinav:
                say = 1
                while say <= sorusayisi:
                    if dcevap[f'C{say}_id'] == 1:
                        cevap_kagidi.append('A')
                    elif dcevap[f'C{say}_id'] == 2:
                        cevap_kagidi.append('B')
                    elif dcevap[f'C{say}_id'] == 3:
                        cevap_kagidi.append('C')
                    elif dcevap[f'C{say}_id'] == 4:
                        cevap_kagidi.append('D')
                    elif dcevap[f'C{say}_id'] == 5:
                        cevap_kagidi.append('E')
                    else:
                        cevap_kagidi.append('girilmemiş')
                    cevaplist.append(dcevap[f'C{say}_id'])
                    say += 1
                cevap_kagidi.append(sorusayisi)
                cevap_kagidi.append(0)
                cevap_kagidi.append(100)

            puanlist = []
            for puan in sorupuan:
                say = 1
                while say <= sorusayisi:
                    puanlist.append(puan[f'P{say}'])
                    say += 1

            for ogr in ogrcevaplar:
                puan = 0
                dogru_sayisi = 0
                yanlis_sayisi = 0
                ogrenci = User.objects.get(id=ogr['ogrenci_id'])
                rapor = [ogrenci.id, ogrenci.first_name, ogrenci.last_name]
                say = 1
                while say <= sorusayisi:
                    if ogr[f'C{say}_id'] is None:
                        rapor.append(0)
                    else:
                        rapor.append(ogr[f'C{say}_id'])
                        if ogr[f'C{say}_id'] == cevaplist[say - 1]:
                            dogru_sayisi += 1
                            puan += puanlist[say - 1]
                        else:
                            yanlis_sayisi += 1
                    say += 1
                rapor.append(dogru_sayisi)
                rapor.append(yanlis_sayisi)
                rapor.append(puan)
                if (ogrenci.id == request.user.id):
                    ogrenci_cevap = rapor.copy()
                raporList.append(rapor)
            raporList = np.array(raporList)
            x = np.array(raporList[:, -1]).astype(np.int32)
        except Exception as e:
            return render(request, 'ogrenci/rapor.html', {'hata': True})
        context = {
            'cevap_kagidi': cevap_kagidi,
            'ogr_cevaplari': ogrenci_cevap,
            'ogr_puan': ogrenci_cevap[-1],
            'yanlis_say': ogrenci_cevap[-2],
            'dogru_say': ogrenci_cevap[-3],
            'sorusayilist': range(1, sorusayisi + 1),
            'sorusayisi': sorusayisi + 3,
            'max_not': x.max(),
            'min_not': x.min(),
            'ortalama': round(np.average(x), 1),
            'sinav_adi': Sinav.objects.get(id=pk).baslik,
        }
        pdf = render_to_pdf('ogrenci/pdf/rapor_pdf.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")
