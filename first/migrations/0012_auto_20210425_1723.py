# Generated by Django 3.1.7 on 2021-04-25 14:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first', '0011_gallery'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProfileAvatars',
            new_name='ProfileAddInfo',
        ),
    ]
