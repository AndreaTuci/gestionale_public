# Generated by Django 3.1 on 2021-10-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amministrazione', '0018_timecardentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='timecardentry',
            name='entry_time',
            field=models.TimeField(auto_now=True, verbose_name='Ora'),
        ),
        migrations.AlterField(
            model_name='timecardentry',
            name='entry_date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
    ]
