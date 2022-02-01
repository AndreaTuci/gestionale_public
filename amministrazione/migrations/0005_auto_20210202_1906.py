# Generated by Django 3.1 on 2021-02-02 18:06

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('amministrazione', '0004_auto_20210202_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacheragreement',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 2, 18, 6, 23, 944168, tzinfo=utc), verbose_name='Data di stipula'),
        ),
        migrations.AlterField(
            model_name='teacheragreement',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data di conclusione'),
        ),
        migrations.AlterField(
            model_name='teacheragreement',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 2, 18, 6, 23, 944287, tzinfo=utc), verbose_name='Data di avvio'),
        ),
    ]