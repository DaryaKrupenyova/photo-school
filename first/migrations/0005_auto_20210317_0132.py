# Generated by Django 3.1.7 on 2021-03-16 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0004_useraccount_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(default=0, max_length=300)),
                ('lesson_num', models.IntegerField(default=0)),
                ('lecture_status', models.IntegerField(default=0)),
                ('homework_status', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='UserAccount',
        ),
    ]
