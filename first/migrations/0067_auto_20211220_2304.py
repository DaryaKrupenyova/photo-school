# Generated by Django 3.1.7 on 2021-12-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0066_auto_20211220_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='part',
            field=models.IntegerField(default=1),
        ),
    ]
