# Generated by Django 3.1 on 2021-07-15 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0044_auto_20210714_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplinaryMeasureRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measure_read', to='anagrafica.disciplinarymeasure', verbose_name='Segnalazione')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_reported_has_read', to='anagrafica.student', verbose_name='Studente')),
            ],
            options={
                'verbose_name': 'Lettura segnalazione',
                'verbose_name_plural': 'Letture segnalazioni',
            },
        ),
    ]
