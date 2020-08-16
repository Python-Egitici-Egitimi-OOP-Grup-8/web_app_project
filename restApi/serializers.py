from rest_framework import serializers
from oturum.models import OgrenciCevap,secenekListe

class OgrenciCevapSerializer(serializers.ModelSerializer):
    eklenmetarihi=serializers.ReadOnlyField()
    class Meta:
        fieldTemp=secenekListe('C')
        fieldTemp.append('ogrenci')
        fieldTemp.append('sinav')
        fieldTemp.append('eklenmetarihi')
        fieldTemp.append('id')
        model=OgrenciCevap
        fields=fieldTemp

