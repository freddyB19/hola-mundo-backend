# Generated by Django 4.0.6 on 2022-08-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_modulo_introduccion_sesion_introduccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='progresoplayer',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]