# Generated by Django 3.1 on 2021-11-14 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0057_student_is_withdrawn'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='badge',
            field=models.SlugField(blank=True, max_length=25, null=True, verbose_name='Codice badge'),
        ),
    ]
