# Generated by Django 3.1.7 on 2021-10-17 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegramapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bugreports',
            name='report_num',
        ),
    ]
