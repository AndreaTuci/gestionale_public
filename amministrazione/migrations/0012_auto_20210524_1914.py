# Generated by Django 3.1 on 2021-05-24 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amministrazione', '0011_warehouse_last_movement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='last_movement',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 24, 19, 14, 19, 205040), verbose_name='Data ultimo movimento'),
        ),
    ]