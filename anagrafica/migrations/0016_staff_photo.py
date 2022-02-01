# Generated by Django 3.1 on 2020-11-23 11:41

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0015_auto_20201120_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='avatar'),
        ),
    ]
