from django.forms import ModelForm
from django.contrib.auth.models import User
from oturum.models import SoruPuanlama, SoruKazanim
from django.contrib.auth.models import User
from oturum.models import *

class SoruPuanForm(ModelForm):
    class Meta:
        model = SoruPuanlama
        exclude = ['sinav']

class KazanimSoru(ModelForm):
    class Meta:
        model = SoruKazanim
        fieldTemp=secenekListe('K')
        fields=fieldTemp
      
    def __init__(self, *args, **kwargs):
        dersid = kwargs.pop('dersid')
        super(KazanimSoru,self).__init__(*args, **kwargs)
        for secenek in secenekListe('K'):
            self.fields[secenek].queryset = Kazanim.objects.filter(ders=dersid.id)
       
        

class Profilim(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class SinavEkle(ModelForm):
    class Meta:
        model = Sinav
        fields = ['baslik','ders','sorusayisi']

class CevapEkle(ModelForm):
    class Meta:
        model = Sinav
        exclude = ['user','baslik','ders','sorusayisi']