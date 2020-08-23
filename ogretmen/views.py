import base64
import io
import urllib

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404


from oturum.models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from django.views.generic import View
from django.template.loader import get_template
from .utilities import render_to_pdf


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
    dersId=sinav.ders
   # print(kazanim.__dict__)
    form = KazanimSoru(instance=kazanim,dersid=dersId)
    context = {
        'sinavbaslik': sinav.baslik,
        'form': form,
        'say': sinav.sorusayisi,
    }
    if request.method == 'POST':
        form = KazanimSoru(request.POST,instance=kazanim,dersid=dersId)
        print(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/ogretmen/sinavlarim')
    return render(request,'ogretmen/kazanimlar.html',context)

def soruPuan(request,pk):
    sinav=Sinav.objects.get(id=pk)
    sorusay = Sinav.objects.get(id=pk).sorusayisi
    puan = SoruPuanlama.objects.get(sinav_id=pk) #Seçilen sınava ait puan değerleri getiriliyor.
    form = SoruPuanForm(instance = puan) #Kullanıcıya görüntülenmek üzere puan değerleri ile form örneği oluşturuluyor.
    context = {
        'sinavbaslik':sinav.baslik,
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
        'sinavbaslik':sinav.baslik,
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
    try:
        kazanimlar = SoruKazanim.objects.filter(sinav_id=pk).values()
        sorusayisi = Sinav.objects.get(id=pk).sorusayisi
        kazanimList = []
        for id in kazanimlar:
            say = 1
            while say <= sorusayisi:
                kazanimList.append(Kazanim.objects.get(id=id[f'K{say}_id']).kazanimadi)
                say += 1
        sinav = Sinav.objects.filter(id=pk).values()
        ogrenciler = OgrenciCevap.objects.filter(sinav_id=pk)
        ogrenci_sayisi=ogrenciler.count()
        ogrcevaplar = ogrenciler.values()
        sinav_ogrenci_say = ogrenciler.count()
        sorupuan = SoruPuanlama.objects.filter(sinav_id=pk).values()
        raporList = []
        cevap_kagidi = [0,request.user.first_name,request.user.last_name]
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
        # print(puanlist)
        soru_no=[i for i in range(1,sorusayisi+1)]
        madde_gucluk = [0 for i in range(sorusayisi)]
        soru_yanlis_say = [0 for i in range(sorusayisi)]
        soru_bos_say = [0 for i in range(sorusayisi)]
        basarili_ogrenci = 0
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
                    soru_bos_say[say-1] += 1
                else:
                    rapor.append(ogr[f'C{say}_id'])
                    if ogr[f'C{say}_id'] == cevaplist[say-1]:
                        dogru_sayisi += 1
                        puan += puanlist[say-1]
                        madde_gucluk[say-1] += 1
                    else:
                        yanlis_sayisi += 1
                        soru_yanlis_say[say-1] += 1
                say += 1
            if(puan>50):
                basarili_ogrenci +=1
            rapor.append(dogru_sayisi)
            rapor.append(yanlis_sayisi)
            rapor.append(puan)
            raporList.append(rapor)
        raporList = np.array(raporList)
        dogru_cevap_say = madde_gucluk.copy()
        say =1
        while say<=sorusayisi:
            madde_gucluk[say - 1] /= sinav_ogrenci_say
            say+=1
        zipped_soru_analiz = zip(soru_no, kazanimList, madde_gucluk, dogru_cevap_say, soru_yanlis_say, soru_bos_say)
        x = np.array(raporList[:, -1]).astype(np.int32)
    except Exception as e:
        print(e)
        return render(request,'ogretmen/rapor.html', {'hata':True})
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    etiketler = ['Başarılı', 'Başarısız']
    ogrenciler = [basarili_ogrenci, ogrenci_sayisi-basarili_ogrenci]
    ax.pie(ogrenciler, labels=etiketler, autopct='%1.2f%%')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    resim_grafik = urllib.parse.quote(string)

    fig = plt.figure()
    plt.bar(soru_no,madde_gucluk,width=0.4)
    plt.xlabel('Sorular')
    plt.ylabel('Güçlük İndeksi')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    gucluk_grafik = urllib.parse.quote(string)
    context={
        'cevap_kagidi': cevap_kagidi,
        'sinav_rapor': raporList,
        'soru_rapor':zipped_soru_analiz,
        'sorusayilist': range(1,sorusayisi+1),
        'sorusayisi':sorusayisi+3,
        'max_not': x.max(),
        'min_not': x.min(),
        'ortalama': round(np.average(x),1),
        'varyans': np.var(x),
        'standart_sapma': round(np.std(x),1),
        'ortanca_değer': np.median(x),
        'basarili_sayisi': basarili_ogrenci,
        'ogrenci_sayisi':ogrenci_sayisi,
        'basarisiz_sayisi':ogrenci_sayisi-basarili_ogrenci,
        'basari_grafik': resim_grafik,
        'gucluk_grafik': gucluk_grafik,
        'sinav_id':pk,
    }
    return render(request,'ogretmen/rapor.html',context)

def tokenAl(request):
    token, created = Token.objects.get_or_create(user_id=request.user.id) #varsa getir yoksa yeni token oluştur.
    context = {'anahtar':token}
    return render(request, 'ogretmen/tokenAl.html',context)

class PDFOlustur(View):
    def get(self, request, pk, *args, **kwargs):
        template = get_template('ogretmen/pdf/rapor_pdf.html')
        try:
            kazanimlar = SoruKazanim.objects.filter(sinav_id=pk).values()
            sorusayisi = Sinav.objects.get(id=pk).sorusayisi
            kazanimList = []
            for id in kazanimlar:
                say = 1
                while say <= sorusayisi:
                    kazanimList.append(Kazanim.objects.get(id=id[f'K{say}_id']).kazanimadi)
                    say += 1
            sinav = Sinav.objects.filter(id=pk).values()
            ogrenciler = OgrenciCevap.objects.filter(sinav_id=pk)
            ogrenci_sayisi = ogrenciler.count()
            ogrcevaplar = ogrenciler.values()
            sinav_ogrenci_say = ogrenciler.count()
            sorupuan = SoruPuanlama.objects.filter(sinav_id=pk).values()
            raporList = []
            cevap_kagidi = [0, request.user.first_name, request.user.last_name]
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
            # print(puanlist)
            soru_no = [i for i in range(1, sorusayisi + 1)]
            madde_gucluk = [0 for i in range(sorusayisi)]
            soru_yanlis_say = [0 for i in range(sorusayisi)]
            soru_bos_say = [0 for i in range(sorusayisi)]
            basarili_ogrenci = 0
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
                        soru_bos_say[say - 1] += 1
                    else:
                        rapor.append(ogr[f'C{say}_id'])
                        if ogr[f'C{say}_id'] == cevaplist[say - 1]:
                            dogru_sayisi += 1
                            puan += puanlist[say - 1]
                            madde_gucluk[say - 1] += 1
                        else:
                            yanlis_sayisi += 1
                            soru_yanlis_say[say - 1] += 1
                    say += 1
                if (puan > 50):
                    basarili_ogrenci += 1
                rapor.append(dogru_sayisi)
                rapor.append(yanlis_sayisi)
                rapor.append(puan)
                raporList.append(rapor)
            raporList = np.array(raporList)
            dogru_cevap_say = madde_gucluk.copy()
            say = 1
            while say <= sorusayisi:
                madde_gucluk[say - 1] /= sinav_ogrenci_say
                say += 1
            zipped_soru_analiz = zip(soru_no, kazanimList, madde_gucluk, dogru_cevap_say, soru_yanlis_say, soru_bos_say)
            x = np.array(raporList[:, -1]).astype(np.int32)
        except Exception as e:
            print(e)
            return render(request, 'ogretmen/pdf/rapor_pdf.html', {'hata': True})
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        etiketler = ['Başarılı', 'Başarısız']
        ogrenciler = [basarili_ogrenci, ogrenci_sayisi - basarili_ogrenci]
        ax.pie(ogrenciler, labels=etiketler, autopct='%1.2f%%')
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        resim_grafik = urllib.parse.quote(string)

        fig = plt.figure()
        plt.bar(soru_no, madde_gucluk, width=0.4)
        plt.xlabel('Sorular')
        plt.ylabel('Güçlük İndeksi')
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        gucluk_grafik = urllib.parse.quote(string)
        context = {
            'cevap_kagidi': cevap_kagidi,
            'sinav_rapor': raporList,
            'soru_rapor': zipped_soru_analiz,
            'sorusayilist': range(1, sorusayisi + 1),
            'sorusayisi': sorusayisi + 3,
            'max_not': x.max(),
            'min_not': x.min(),
            'ortalama': round(np.average(x), 1),
            'varyans': np.var(x),
            'standart_sapma': round(np.std(x), 1),
            'ortanca_değer': np.median(x),
            'basarili_sayisi': basarili_ogrenci,
            'ogrenci_sayisi': ogrenci_sayisi,
            'basarisiz_sayisi': ogrenci_sayisi - basarili_ogrenci,
            'basari_grafik': resim_grafik,
            'gucluk_grafik': gucluk_grafik,
            'sinav_baslik': Sinav.objects.get(id=pk).baslik
        }
        pdf = render_to_pdf('ogretmen/pdf/rapor_pdf.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")