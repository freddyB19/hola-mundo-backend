# Generated by Django 4.0.6 on 2022-08-22 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_progresoperson_next'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sesion',
            options={'ordering': ['id'], 'verbose_name': 'Sesion', 'verbose_name_plural': 'Sesiones'},
        ),
    ]
