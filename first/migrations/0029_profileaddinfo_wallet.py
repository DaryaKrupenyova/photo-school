# Generated by Django 3.1.7 on 2021-08-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0028_imagesfromhomeworks_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddinfo',
            name='wallet',
            field=models.IntegerField(default=0),
        ),
    ]
