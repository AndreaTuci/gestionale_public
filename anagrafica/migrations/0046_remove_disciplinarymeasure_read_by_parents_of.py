# Generated by Django 3.1 on 2021-07-15 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0045_disciplinarymeasureread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disciplinarymeasure',
            name='read_by_parents_of',
        ),
    ]