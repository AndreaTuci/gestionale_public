# Generated by Django 3.1 on 2020-12-23 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0021_auto_20201202_1021'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FooModel',
        ),
        migrations.AlterField(
            model_name='staff',
            name='contract_hours',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Ore da contratto (seetimanali)'),
        ),
        migrations.AlterField(
            model_name='student',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Numero sul registro'),
        ),
    ]
