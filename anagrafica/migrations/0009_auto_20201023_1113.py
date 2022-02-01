# Generated by Django 3.1 on 2020-10-23 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0008_auto_20200807_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attended_curriculum', to='anagrafica.course', verbose_name='Corso frequentato'),
        ),
    ]
