# Generated by Django 3.1 on 2021-12-14 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0059_auto_20211115_1030'),
        ('frequenze', '0029_lessonwithdate'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonwithdate',
            unique_together={('lesson_date', 'hour', 'training_unit')},
        ),
    ]
