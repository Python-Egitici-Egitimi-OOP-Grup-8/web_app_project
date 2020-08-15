from django.shortcuts import render

from django.http import HttpResponse
def restapideneme(request):
    return HttpResponse('<h1>Rest Api Deneme Sayfasına Hoşa geldiniz</h1>')
