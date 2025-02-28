from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Be Rural está funcionando correctamente!")
