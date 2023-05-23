from django.shortcuts import render, redirect
from django.http import HttpRequest
from pathlib import Path

from clonus.forms import FileToFileForm
from clonus.models import Package

from clonus.methods.fp_method_builder import FingerprintMethodBuilder
from clonus.methods.method_configurator import MethodConfigurator

# Create your views here.


def index(request: HttpRequest):
    return render(request, "index.html")


def compare(request: HttpRequest):
    if request.method == "POST":
        form = FileToFileForm(request.POST, request.FILES)
        if form.is_valid():
            p = Package(
                gram_size=request.POST["gram_size"],
                window_size=request.POST["window_size"],
            )
            p.save()
            p.mkdir()
            for file in (request.FILES["file1"], request.FILES["file2"]):
                with open(p.path / file.name, "wb+") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            p.file1 = p.path / request.FILES["file1"].name
            p.file2 = p.path / request.FILES["file2"].name
            p.gen_hash()
            p.save()
            return redirect("summary", h=p.hash)

    else:
        form = FileToFileForm()
    context = {"form": form}
    return render(request, "send.html", context)


def summary(request: HttpRequest, h: str):
    try:
        p = Package.objects.get(hash=h)
    except Package.DoesNotExist:
        return redirect("index")
    if not p.processed:
        filenames = [p.file1, p.file2]
        fp_builder = FingerprintMethodBuilder(filenames, p.gram_size, p.window_size)
        config = MethodConfigurator(fp_builder)
        method_res = config.make_method()
        # method_res.print()
        # p.coeff = round(method_res.clone_pct * 100,2)
        p.coeff = method_res.clone_pct
        p.processed = True
        p.save()
    
    with open(p.file1, 'r', encoding='utf-8') as f:
        file1 = f.read()
    
    with open(p.file2, 'r', encoding='utf-8') as f:
        file2 = f.read()

    context = {
        "hash": p.hash,
        "coeff": p.coeff*100,
        "file1": file1,
        "file2": file2,
        "f1": Path(p.file1).name,
        "f2": Path(p.file2).name
    }
    return render(request, "summary.html", context)


def list(request: HttpRequest):
    q = Package.objects.all().order_by("-date")
    context = {
        "packages": ((i, Path(i.file1).name, Path(i.file2).name) for i in q)
    }
    return render(request, "list.html", context)
