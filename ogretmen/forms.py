from django.forms import ModelForm
from django.contrib.auth.models import User
from oturum.models import SoruPuanlama, SoruKazanim
from django.contrib.auth.models import User
from oturum.models import *

class SoruPuanForm(ModelForm):
    class Meta:
        model = SoruPuanlama
        fields = '__all__'

class KazanimSoru(ModelForm):
    class Meta:
        model = SoruKazanim
        fields = '__all__'

class Profilim(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class SinavEkle(ModelForm):
    class Meta:
        model = Sinav
        fields = ['baslik','ders','sorusayisi']

