# Generated by Django 3.1.7 on 2021-09-09 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0032_transactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='till',
            new_name='sum',
        ),
    ]
