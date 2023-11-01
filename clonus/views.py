from django.shortcuts import render, redirect
from django.http import HttpRequest

from clonus.forms import FileToFileForm
from clonus.models import Package

from clonus.methods.fp_method_builder import FingerprintMethodBuilder
from clonus.methods.method_configurator import MethodConfigurator

# Create your views here.


def index(request: HttpRequest):
    return render(request, "index.html")


def f2f(request: HttpRequest):
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
            return redirect("f2f_summary", h=p.hash)

    else:
        form = FileToFileForm()
    context = {"title": "Сравнение двух файлов", "form": form}
    return render(request, "send.html", context)


def f2f_summary(request: HttpRequest, h: str):
    try:
        p = Package.objects.get(hash=h)
    except Package.DoesNotExist:
        return redirect("index")
    if not p.processed:
        filenames = [p.file1, p.file2]
        fp_builder = FingerprintMethodBuilder(filenames, p.gram_size, p.window_size)
        config = MethodConfigurator(fp_builder)
        res = config.make_method()
        res.print()
        p.processed = True
        p.save()
        # TODO: 
        # 1). save shit to db
        # 2). interpolate files with html tags
        # 3). write view for summary
        # 4). think of a way to implement f2db
    return render(request, "f2f_summary.html")


def f2db(request: HttpRequest):
    pass
