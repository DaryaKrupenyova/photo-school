# Generated by Django 3.1.7 on 2021-09-29 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0052_auto_20210929_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='course_num',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='first.courses'),
        ),
    ]
