# Generated by Django 3.1 on 2020-11-23 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0017_auto_20201123_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='picture',
        ),
        migrations.AlterField(
            model_name='staff',
            name='task',
            field=models.CharField(choices=[('A', 'Altro'), ('D', 'Docente'), ('T', 'Tutor'), ('S', 'Segreteria'), ('C', 'Coordinamento'), ('P', 'Direzione')], max_length=20, verbose_name='Mansione'),
        ),
    ]