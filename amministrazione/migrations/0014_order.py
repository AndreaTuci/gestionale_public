# Generated by Django 3.1 on 2021-05-28 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amministrazione', '0013_auto_20210524_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique_for_year=True, verbose_name='Numero di ordine')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Quantità')),
                ('notes', models.CharField(blank=True, max_length=256, null=True, verbose_name='Note')),
                ('order_placed_at', models.DateTimeField(auto_now=True, verbose_name='Data di ordine')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ordered', to='amministrazione.warehouse', verbose_name='Prodotto')),
            ],
            options={
                'verbose_name': 'Ordine',
                'verbose_name_plural': 'Ordini',
            },
        ),
    ]