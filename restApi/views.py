from django.shortcuts import render
from rest_framework import generics,permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.http  import JsonResponse
from oturum.models import OgrenciCevap,Sinav
from rest_framework.exceptions import  ValidationError
from .serializers import OgrenciCevapSerializer
@csrf_exempt
def login(request):
    
    if request.method == 'POST':
        
        data=JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
                 return JsonResponse({'error':'Login olamadiniz lütfen bilgilerinizi kontrol ediniz..'},status=400)
        else:
            if is_ogretmen(user):
                try:
                    token=Token.objects.get(user=user)
                except:
                    token=Token.objects.create(user=user)
                return JsonResponse({'token':str(token)},status=201)
            else:
                return JsonResponse({'optik formda kullanilacak id':str(user.id)},status=201)

@csrf_exempt
def signup(request):
    
    if request.method == 'POST':
        try:
            data=JSONParser().parse(request)
            
            grupAdi=data['rol']
            if grupAdi=="ogretmen" or grupAdi=="ogrenci":
                user = User.objects.create_user(data['username'], password=data['password'])
                user.save()
                token=Token.objects.create(user=user)
                usergrup, created = Group.objects.get_or_create(name=grupAdi)    
                user.groups.add(usergrup)
                if grupAdi=="ogretmen":
                    return JsonResponse({'token':str(token)},status=201)
                else:
                    return JsonResponse({'id':str(user.id)},status=201)
            else:
               return JsonResponse({'error':'Uyelik Basarisiz. Lutfen grup adini dogru yaziniz..'},status=400)
            
        except IntegrityError:
            return JsonResponse({'error':'Bu kullanici daha once olusuturuldu lutfen yeni kullanici secin'},status=400)


def is_ogretmen(user):
    return user.groups.filter(name='ogretmen').exists()
def is_ogrenci(user):
    return user.groups.filter(name='ogrenci').exists()

def restapideneme(request):
    return HttpResponse('<h1>Rest Api Deneme Sayfasına Hoşa geldiniz</h1>')

class OgrenciCevapList(generics.ListAPIView):
    serializer_class = OgrenciCevapSerializer
    #permission_classes sonundaki es takısı kalkarsa yetkisiz erişimde hata verir.
    #permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        #user=self.request.user
        return OgrenciCevap.objects.all()

class OgrenciCevapEkle(generics.ListCreateAPIView):
    serializer_class = OgrenciCevapSerializer
    #permission_classes sonundaki es takısı kalkarsa yetkisiz erişimde hata verir.
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        #user=self.request.user
        return OgrenciCevap.objects.all()

    def perform_create(self,serializer):
        #print("HATA_MESAJI: "+str(serializer.data['sinav']))
        ogrenci=serializer.validated_data.get('ogrenci')
        sinav=serializer.validated_data.get('sinav')
        user=self.request.user
        if Sinav.objects.filter(user=user,id=int(sinav.id)):
            user1=User.objects.filter(id=int(ogrenci.id))
            if (user1):
                ogrencicevap=OgrenciCevap.objects.filter(ogrenci=ogrenci.id,sinav=sinav.id)
                if ogrencicevap:
                     raise ValidationError('Öğrenci bu sınava daha önce cevap gönderdi.')
                else:            
                    serializer.save()
            else:
                raise ValidationError('Öğrenci kayılı değil tc no yanlış yazılmış olabilir..')
        else:
            raise ValidationError('Eklemeye çalıştığınız Sınav Size ait Değil Sınav kodu yanlış olabilir..')
        
  