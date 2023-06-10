from django.shortcuts import render, redirect
from django.http import HttpRequest
from pathlib import Path
from collections import deque
from itertools import combinations
from more_itertools import ilen

from clonus.forms import FileToFileForm, ManyFilesForm
from clonus.models import Package, MultiPackage

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


def compare_many(request: HttpRequest):
    if request.method == "POST":
        form = ManyFilesForm(request.POST, request.FILES)
        if form.is_valid():
            p = MultiPackage(
                gram_size=request.POST["gram_size"],
                window_size=request.POST["window_size"],
            )
            p.save()
            p.mkdir()
            for file in request.FILES.getlist("files"):
                with open(p.path / file.name, "wb+") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            p.files = p.path
            p.gen_hash()
            p.save()
            return redirect("summary", h=p.hash)

    else:
        form = ManyFilesForm()
    context = {"form": form}
    return render(request, "send_many.html", context)


def process_file(fil: Path, l: "list[list[int]]"):
    res = []
    pos = 0
    contents = ""
    line_count = 0
    offsets = deque(l)
    cur = offsets[0][0]
    end_of_q = False
    with open(fil, "r", encoding="utf-8") as f:
        for line in f:
            contents += line
            line_count += 1
            pos += len(line)
            if pos >= cur and not end_of_q:
                if cur == offsets[0][0]:
                    cur = offsets[0][1]
                    res.append([line_count, line_count])
                else:
                    offsets.popleft()
                    try:
                        cur = offsets[0][0]
                    except IndexError:
                        end_of_q = True
                    res[-1][-1] = line_count
        # print(res)
    return contents, res


def summary(request: HttpRequest, h: str):
    try:
        p = Package.objects.get(hash=h)
    except Package.DoesNotExist:
        return redirect("index")

    filenames = [p.file1, p.file2]
    fp_builder = FingerprintMethodBuilder(filenames, p.gram_size, p.window_size)
    config = MethodConfigurator(fp_builder)
    method_res = config.make_method()
    p.coeff = method_res.clone_pct
    p.processed = True
    p.save()

    file1, q1 = process_file(p.file1, method_res.clone_parts_1)
    file2, q2 = process_file(p.file2, method_res.clone_parts_2)

    context = {
        "hash": p.hash,
        "coeff": p.coeff * 100,
        "file1": file1,
        "file2": file2,
        "f1": Path(p.file1).name,
        "f2": Path(p.file2).name,
        "q1": ", ".join(
            "{start: " + str(i) + ", end: " + str(j) + ", color: 'yellow'}"
            for i, j in q1
        ),
        "q2": ", ".join(
            "{start: " + str(i) + ", end: " + str(j) + ", color: 'yellow'}"
            for i, j in q2
        ),
    }
    return render(request, "summary.html", context)


def summary_many(request: HttpRequest, h: str):
    try:
        p = MultiPackage.objects.get(hash=h)
    except MultiPackage.DoesNotExist:
        return redirect("index")

    contents = []
    names = []

    for file in Path(p.path).iterdir():
        with open(file, "r", encoding="utf8") as f:
            names.append(file.name)
            contents.append(f.read())

    names1 = []
    names2 = []
    coeffs = []
    for f1, f2 in combinations(Path(p.path).iterdir(), 2):
        fp_builder = FingerprintMethodBuilder([f1, f2], p.gram_size, p.window_size)
        config = MethodConfigurator(fp_builder)
        method_res = config.make_method()
        coeffs.append(method_res.clone_pct * 100)
        p.processed = True
        p.save()
        names1.append(f1.name)
        names2.append(f2.name)

    context = {
        "hash": p.hash,
        "data1": zip(names, contents),
        "data2": zip(coeffs, names1, names2),
    }
    return render(request, "summary_many.html", context)


def list(request: HttpRequest):
    q1 = Package.objects.all().order_by("-date")
    q2 = MultiPackage.objects.all().order_by("-date")
    context = {
        "packages": ((i, Path(i.file1).name, Path(i.file2).name) for i in q1),
        "multipackages": (
            (i, f"Количество файлов: {ilen(Path(i.path).iterdir())}") for i in q2
        ),
    }
    return render(request, "list.html", context)
