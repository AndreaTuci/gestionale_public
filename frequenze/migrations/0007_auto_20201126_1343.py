# Generated by Django 3.1 on 2020-11-26 12:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0020_staff_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frequenze', '0006_notes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notes',
            new_name='Note',
        ),
    ]