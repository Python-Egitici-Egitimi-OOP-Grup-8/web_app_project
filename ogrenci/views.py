from django.shortcuts import render
from django.http import HttpResponse

def ogrencideneme(request):
    return render(request, 'ogrenci/ogrencideneme.html')
