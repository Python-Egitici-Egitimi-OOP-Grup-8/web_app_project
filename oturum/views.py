from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'oturum/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'oturum/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                usergroup, created = Group.objects.get_or_create(name=request.POST['rol'] )
                user.groups.add(usergroup)
                login(request, user)
                if request.POST['rol']=="ogretmen":
                    return redirect('/ogretmen/')
                else:
                    return redirect('/ogrenci/')
            except IntegrityError:
                return render(request, 'oturum/signupuser.html', {'form':UserCreationForm(), 'error':'Bu kullanıcı daha önce oluşturuldu lütfen başka bir kullanıcı adı seçiniz!'})
        else:
            return render(request, 'oturum/signupuser.html', {'form':UserCreationForm(), 'error':'Şifreler Eşleşmiyor'})

def is_ogretmen(user):
        return user.groups.filter(name='ogretmen').exists()
        
def is_ogrenci(user):
        return user.groups.filter(name='ogrenci').exists()

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'oturum/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'oturum/loginuser.html', {'form':AuthenticationForm(), 'error':'Kullanıcı adı veya Şifre Hatalı'})
        else:
            login(request, user)
            if is_ogretmen(user):
                return redirect('/ogretmen/')
            else:
                return redirect('/ogrenci/')
        
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    