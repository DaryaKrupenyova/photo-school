# Generated by Django 3.1.7 on 2021-12-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0068_auto_20211222_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image_compressed',
            field=models.ImageField(default='', upload_to='gallery_compressed'),
        ),
    ]
