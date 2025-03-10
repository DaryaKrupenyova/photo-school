# Generated by Django 3.1.7 on 2021-11-13 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0061_auto_20211113_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='pdf_route',
            field=models.FileField(default=0, upload_to='pdf'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='expires',
            field=models.DateField(default=datetime.date(2021, 11, 15)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='was',
            field=models.DateField(default='14/11/2021'),
        ),
    ]
