# Generated by Django 3.1.7 on 2021-09-09 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0036_auto_20210909_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='was',
            field=models.DateField(default='2021-09-09'),
        ),
    ]
