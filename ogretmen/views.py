from django.shortcuts import render
from django.http import HttpResponse

def ogretmenIndex(request):
    return render(request, 'ogretmen/ogretmenIndex.html')

def sinavlarim(request):
    return render(request, 'ogretmen/sinavlarim.html')

def profile(request):
    return render(request, 'ogretmen/profile.html')

def tokenAl(request):
    return render(request, 'ogretmen/tokenAl.html')