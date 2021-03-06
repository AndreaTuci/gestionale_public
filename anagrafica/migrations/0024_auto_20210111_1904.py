# Generated by Django 3.1 on 2021-01-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0023_auto_20210108_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='chief_legal_birth',
            field=models.DateField(blank=True, null=True, verbose_name='RL - Data di nascita'),
        ),
        migrations.AlterField(
            model_name='company',
            name='chief_legal_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='RL - Nome'),
        ),
        migrations.AlterField(
            model_name='company',
            name='chief_legal_place_of_birth',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='RL - Nato a'),
        ),
        migrations.AlterField(
            model_name='company',
            name='chief_legal_resident_in',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='RL - Residente in'),
        ),
        migrations.AlterField(
            model_name='company',
            name='chief_legal_role',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='RL - In qualità di'),
        ),
        migrations.AlterField(
            model_name='company',
            name='chief_legal_surname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Responsabile legale - Cognome'),
        ),
        migrations.AlterField(
            model_name='company',
            name='commerce_registration',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Iscrizione Camera di Commercio N°'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_contact',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Referente aziendale'),
        ),
        migrations.AlterField(
            model_name='company',
            name='operational_headquarters_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sede operativa - Indirizzo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='operational_headquarters_city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sede operativa - Comune'),
        ),
        migrations.AlterField(
            model_name='company',
            name='registered_office_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sede legale - Indirizzo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='registered_office_city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sede legale - Comune'),
        ),
        migrations.AlterField(
            model_name='company',
            name='vat',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='P. IVA'),
        ),
    ]
