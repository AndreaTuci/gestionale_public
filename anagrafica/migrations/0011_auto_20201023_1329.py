# Generated by Django 3.1 on 2020-10-23 11:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0010_auto_20201023_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Data di iscrizione'),
        ),
    ]