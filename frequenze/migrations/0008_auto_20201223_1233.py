# Generated by Django 3.1 on 2020-12-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0007_auto_20201126_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_text',
            field=models.CharField(max_length=280, verbose_name='Testo'),
        ),
    ]