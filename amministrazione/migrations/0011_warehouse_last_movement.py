# Generated by Django 3.1 on 2021-05-24 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amministrazione', '0010_auto_20210524_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='last_movement',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Data ultimo movimento'),
        ),
    ]