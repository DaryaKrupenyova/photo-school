# Generated by Django 3.1.7 on 2021-03-03 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_auto_20210303_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='email',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='phone',
            field=models.CharField(default=0, max_length=1000),
        ),
    ]
