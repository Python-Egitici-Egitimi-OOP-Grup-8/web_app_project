from django.forms import ModelForm
from oturum.models import *

class Profilim(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
