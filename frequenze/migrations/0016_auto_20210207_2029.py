# Generated by Django 3.1 on 2021-02-07 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequenze', '0015_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='hour',
            field=models.CharField(choices=[('1', '08.00-9.00'), ('2', '09.00-10.00'), ('3', '10.00-11.00'), ('4', '11.00-12.00'), ('5', '12.00-13.00'), ('6', '13.00-14.00'), ('7', '14.00-15.00'), ('8', '15.00-16.00'), ('9', '16.00-17.00')], max_length=12, verbose_name='Ora'),
        ),
    ]
