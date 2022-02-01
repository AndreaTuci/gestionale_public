# Generated by Django 3.1 on 2021-12-15 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0059_auto_20211115_1030'),
        ('frequenze', '0030_auto_20211214_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonDone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_date', models.DateField(verbose_name='Data della lezione')),
                ('hour', models.IntegerField(choices=[(1, '08.00-09.00'), (2, '09.00-10.00'), (3, '10.00-11.00'), (4, '11.00-12.00'), (5, '12.00-13.00'), (6, '13.00-14.00'), (7, '14.00-15.00'), (8, '15.00-16.00'), (9, '16.00-17.00')], verbose_name='Ora')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_lesson_done', to='anagrafica.staff', verbose_name='Docente')),
                ('training_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uf_lesson_done', to='anagrafica.trainingunit', verbose_name='Unità Formativa')),
            ],
            options={
                'verbose_name': 'Lezione svolta',
                'verbose_name_plural': 'Lezioni svolte',
                'unique_together': {('lesson_date', 'hour', 'training_unit')},
            },
        ),
    ]