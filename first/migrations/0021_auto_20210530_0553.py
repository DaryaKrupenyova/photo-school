# Generated by Django 3.1.7 on 2021-05-30 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0020_homework_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='first_name',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='homework',
            name='last_name',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
