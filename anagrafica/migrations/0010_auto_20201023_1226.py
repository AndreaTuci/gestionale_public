# Generated by Django 3.1 on 2020-10-23 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0009_auto_20201023_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome del corso'),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attended_curriculum', to='anagrafica.course', verbose_name='Corso frequentato'),
            preserve_default=False,
        ),
    ]