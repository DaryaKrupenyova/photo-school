# Generated by Django 3.1.7 on 2021-04-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0012_auto_20210425_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddinfo',
            name='telegram_id',
            field=models.IntegerField(default=0),
        ),
    ]
