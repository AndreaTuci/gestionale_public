# Generated by Django 3.1 on 2021-02-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0035_auto_20210204_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='stage_objectives',
            field=models.TextField(blank=True, verbose_name='Obiettivi stage'),
        ),
    ]
