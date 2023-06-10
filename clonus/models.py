from shutil import rmtree
from pathlib import Path
from hashlib import md5
from django.db import models
import django.db.models.signals as si
from django.dispatch import receiver

# Create your models here.


class Package(models.Model):
    id: int
    file1 = models.FilePathField(null=True)
    file2 = models.FilePathField(null=True)
    path = models.FilePathField()
    hash = models.CharField(max_length=32)
    gram_size = models.PositiveSmallIntegerField(default=8)
    window_size = models.PositiveSmallIntegerField(default=3)
    coeff = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def gen_hash(self, chunk_size: int = 4096):
        hasher = md5(str(self.path).encode("utf-8"))
        self.path: Path
        for file in self.path.iterdir():
            with open(file, "rb") as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
        self.hash = hasher.hexdigest()

    def mkdir(self):
        self.path.mkdir()

    def rmdir(self):
        rmtree(self.path)


class MultiPackage(models.Model):
    id: int
    files = models.FilePathField(null=True)
    path = models.FilePathField()
    hash = models.CharField(max_length=32)
    gram_size = models.PositiveSmallIntegerField(default=8)
    window_size = models.PositiveSmallIntegerField(default=3)
    coeff = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def gen_hash(self, chunk_size: int = 4096):
        hasher = md5(str(self.path).encode("utf-8"))
        self.path: Path
        for file in self.path.iterdir():
            with open(file, "rb") as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
        self.hash = hasher.hexdigest()

    def mkdir(self):
        self.path.mkdir()

    def rmdir(self):
        rmtree(self.path)

@receiver(si.post_save, sender=Package)
def post_save_package(sender, instance: Package, created, **kwargs):
    instance.path = Path("packages") / str(instance.id)


@receiver(si.post_save, sender=MultiPackage)
def post_save_multi_package(sender, instance: MultiPackage, created, **kwargs):
    instance.path = Path("packages") / f'{instance.id}m'
