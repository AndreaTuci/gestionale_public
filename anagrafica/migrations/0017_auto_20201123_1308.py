# Generated by Django 3.1 on 2020-11-23 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0016_staff_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='photo',
            new_name='avatar',
        ),
    ]
