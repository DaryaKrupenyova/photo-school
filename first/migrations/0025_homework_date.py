# Generated by Django 3.1.7 on 2021-05-30 06:43

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0024_lesson_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='date',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
    ]
