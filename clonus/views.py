from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.

def index(request: HttpRequest):
    return render(request, 'index.html')

def f2f(request: HttpRequest):
    pass

def f2db(request: HttpRequest):
    pass