from django.shortcuts import render, redirect
from django.http import HttpRequest

from clonus.forms import FileToFileForm

# Create your views here.


def index(request: HttpRequest):
    return render(request, "index.html")


def f2f(request: HttpRequest):
    if request.method == "POST":
        form = FileToFileForm(request.POST, request.FILES)
        if form.is_valid():
            ...
            return redirect("index")
    else:
        form = FileToFileForm()
    context = {"title": "Сравнение двух файлов", "form": form}
    return render(request, "send.html", context)


def f2db(request: HttpRequest):
    pass
