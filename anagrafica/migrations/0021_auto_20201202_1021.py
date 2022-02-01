# Generated by Django 3.1 on 2020-12-02 09:21

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0020_staff_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='INPS',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='inps'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='IRPEF',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='irpef'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='curriculum',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='cv'),
        ),
    ]
