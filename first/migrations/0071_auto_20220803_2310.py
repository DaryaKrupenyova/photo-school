# Generated by Django 3.2.6 on 2022-08-03 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0070_auto_20220406_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddinfo',
            name='about',
            field=models.CharField(default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='promo',
            name='expires',
            field=models.DateField(default=datetime.date(2022, 8, 4)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='was',
            field=models.DateField(default='03/08/2022'),
        ),
    ]
