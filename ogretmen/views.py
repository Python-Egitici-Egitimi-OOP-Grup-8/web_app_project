from django.shortcuts import render
from django.http import HttpResponse

def ogretmendeneme(request):
    return render(request, 'ogretmen/ogretmendeneme.html')