# Generated by Django 3.1 on 2020-11-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0014_staff_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='picture',
            field=models.ImageField(default='profile_images/default_user.png', upload_to='profile_images', verbose_name='Immagine profilo'),
        ),
    ]