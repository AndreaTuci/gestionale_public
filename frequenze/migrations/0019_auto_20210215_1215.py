# Generated by Django 3.1 on 2021-02-15 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0018_auto_20210207_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherattendance',
            name='hours_attended',
        ),
        migrations.RemoveField(
            model_name='teacherattendance',
            name='topic',
        ),
    ]
