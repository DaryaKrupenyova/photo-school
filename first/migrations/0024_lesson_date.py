# Generated by Django 3.1.7 on 2021-05-30 06:34

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0023_auto_20210530_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='date',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
    ]
