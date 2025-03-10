# Generated by Django 3.1.7 on 2021-09-19 19:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first', '0047_auto_20210916_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='expires',
            field=models.DateField(default=datetime.date(2021, 9, 20)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='was',
            field=models.DateField(default='19/09/2021'),
        ),
        migrations.CreateModel(
            name='PromoUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what_promo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='promo', to='first.promo')),
                ('who_use', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
