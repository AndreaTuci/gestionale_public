# Generated by Django 3.1 on 2021-05-19 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0020_note_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='reminder_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Data promemoria'),
        ),
    ]