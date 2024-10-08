from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def Home (request):
    print("hello word")
    return HttpResponse ("Hola mundo")