# Generated by Django 3.1 on 2021-01-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0009_auto_20210108_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='priority',
            field=models.BooleanField(default=False, verbose_name='Importante'),
        ),
    ]