# Generated by Django 3.1 on 2021-05-13 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0040_stage_holidays'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='official_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Nome ufficiale del corso'),
        ),
    ]
