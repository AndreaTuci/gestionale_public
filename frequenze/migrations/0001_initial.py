# Generated by Django 3.0.1 on 2020-07-29 11:10

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anagrafica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('hours_attended', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(1)], verbose_name='Ore')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_teacher', to='anagrafica.Staff', verbose_name='Docente')),
                ('training_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_reference_unit', to='anagrafica.TrainingUnit', verbose_name='UF')),
            ],
            options={
                'verbose_name': 'Presenza docente',
                'verbose_name_plural': 'Presenze docente',
            },
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('hours_attended', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(1)], verbose_name='Ore')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_student', to='anagrafica.Student', verbose_name='Allievo')),
                ('training_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_reference_unit', to='anagrafica.TrainingUnit', verbose_name='UF')),
            ],
            options={
                'verbose_name': 'Presenza allievo',
                'verbose_name_plural': 'Presenze allievo',
            },
        ),
    ]
