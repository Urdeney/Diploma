# Generated by Django 4.2.1 on 2023-05-23 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file1', models.FilePathField(null=True)),
                ('file2', models.FilePathField(null=True)),
                ('path', models.FilePathField()),
                ('hash', models.CharField(max_length=32)),
                ('gram_size', models.PositiveSmallIntegerField(default=8)),
                ('window_size', models.PositiveSmallIntegerField(default=3)),
                ('coeff', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
