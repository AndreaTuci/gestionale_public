# Generated by Django 3.1 on 2021-07-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0052_auto_20210727_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='schedule_name',
            field=models.CharField(help_text='Es. LAB-ELE1', max_length=15, null=True, unique=True, verbose_name='Nome per orario'),
        ),
    ]
