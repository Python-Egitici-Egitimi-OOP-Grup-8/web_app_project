from django.forms import ModelForm
from oturum.models import SoruPuanlama
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class SoruPuanForm(ModelForm):
    class Meta:
        model = SoruPuanlama
        fields = '__all__'