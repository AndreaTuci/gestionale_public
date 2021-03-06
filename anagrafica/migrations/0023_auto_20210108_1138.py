# Generated by Django 3.1 on 2021-01-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0022_auto_20201223_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['registered_office_city'], 'verbose_name': 'Ditta', 'verbose_name_plural': 'Ditte'},
        ),
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['date'], 'verbose_name': 'Convenzione', 'verbose_name_plural': 'Convenzioni'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['type', 'sector', 'name'], 'verbose_name': 'Corso', 'verbose_name_plural': 'Corsi'},
        ),
        migrations.AlterModelOptions(
            name='coursetype',
            options={'ordering': ['course_type'], 'verbose_name': 'Tipologia di corso', 'verbose_name_plural': 'Tipologie di corso'},
        ),
        migrations.AlterModelOptions(
            name='disciplinarymeasure',
            options={'ordering': ['reporting_date'], 'verbose_name': 'Provvedimento disciplinare', 'verbose_name_plural': 'Provvedimenti disciplinari'},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ['sector_name'], 'verbose_name': 'Settore', 'verbose_name_plural': 'Settori'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['surname'], 'verbose_name': 'Personale', 'verbose_name_plural': 'Personale'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['surname'], 'verbose_name': 'Studente', 'verbose_name_plural': 'Studenti'},
        ),
        migrations.AlterModelOptions(
            name='trainingunit',
            options={'ordering': ['code'], 'verbose_name': 'Unità formativa', 'verbose_name_plural': 'Unità formative'},
        ),
        migrations.RemoveField(
            model_name='disciplinarymeasure',
            name='student',
        ),
        migrations.AddField(
            model_name='disciplinarymeasure',
            name='students',
            field=models.ManyToManyField(blank=True, default='', to='anagrafica.Student', verbose_name='Allievi'),
        ),
    ]
