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
    def __init__(self,sorusay, id=None, **kwargs):
        super(KazanimSoru, self).__init__(**kwargs)
        if id:
            say=1
            while say<=sorusay:
                self.fields[f'K{say}'].queryset = Kazanim.objects.filter(ders_id=id)
                say+=1
    class Meta:
        model = SoruKazanim
        exclude = ['sinav']
        # fields='__all__'

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