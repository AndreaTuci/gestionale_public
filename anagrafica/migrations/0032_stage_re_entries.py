# Generated by Django 3.1 on 2021-02-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0031_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='re_entries',
            field=models.TextField(blank=True, verbose_name='Rientri a scuola'),
        ),
    ]
