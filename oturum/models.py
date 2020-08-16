from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Ders(models.Model):
    dersadi = models.CharField(max_length=50)

    def __str__(self):
         return self.dersadi

class Kazanim(models.Model):
    kazanimadi = models.CharField(max_length=150)
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)

    def __str__(self):
         return self.ders.dersadi+":"+self.kazanimadi

class Cevap(models.Model):
    cevap=models.CharField(max_length=1)
    
    def __str__(self):
        return "cevap: "+self.cevap

def  secenekListe(char):
    secenekliste=[]
    for i in range(1,51):
        secenekliste.append(char+str(i))
    return secenekliste

class Sinav(models.Model):
    baslik = models.CharField(max_length=200)
    olusturulmatarihi = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    sorusayisi=models.IntegerField()

    for secenek in secenekListe('C'):
        locals()[secenek] = models.ForeignKey(Cevap, related_name=secenek,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.baslik+"  "+str(self.olusturulmatarihi)

class SoruPuanlama(models.Model):
    sinav =models.ForeignKey(Sinav, on_delete=models.CASCADE)
    for secenek in secenekListe('P'):
        locals()[secenek] = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.sinav.baslik+"  "+str(self.sinav.olusturulmatarihi)        

class SoruKazanim(models.Model):
    sinav = models.ForeignKey(Sinav, on_delete=models.CASCADE)
    for secenek in secenekListe('K'):
         locals()[secenek] = models.ForeignKey(Kazanim, related_name=secenek,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.sınav.baslik+"  "+str(self.sinav.olusturulmatarihi)

class OgrenciCevap(models.Model):
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE)
    sinav =models.ForeignKey(Sinav, on_delete=models.CASCADE)
    eklenmetarihi = models.DateTimeField(auto_now_add=True)
    for secenek in secenekListe('C'):
         locals()[secenek] = models.ForeignKey(Cevap, related_name=('C'+secenek),on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.ogrenci.username +" "+self.sinav.baslik

class OgrenciPuan(models.Model):
    sinav =models.ForeignKey(Sinav, on_delete=models.CASCADE)
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE)
    for secenek in secenekListe('C'):
        locals()[secenek] = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.ogrenci.username +" "+self.sinav.baslik 