# Generated by Django 3.1.7 on 2021-10-17 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BugReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1)),
                ('report_num', models.IntegerField(default=0)),
            ],
        ),
    ]
