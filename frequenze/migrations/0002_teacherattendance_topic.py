# Generated by Django 3.0.8 on 2020-08-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherattendance',
            name='topic',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Argomento'),
        ),
    ]