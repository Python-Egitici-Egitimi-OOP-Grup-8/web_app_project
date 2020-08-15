from django.contrib import admin
from .models import Ders,Kazanim,Cevap,Sinav,SoruPuanlama,SoruKazanim,OgrenciCevap,OgrenciPuan
# Register your models here.
admin.site.register(Ders)
admin.site.register(Kazanim)
admin.site.register(Cevap)
admin.site.register(Sinav)
admin.site.register(SoruPuanlama)
admin.site.register(SoruKazanim)
admin.site.register(OgrenciCevap)
admin.site.register(OgrenciPuan)