# Generated by Django 5.1.2 on 2024-10-26 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_soiled', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='moisure_percent',
            new_name='moisture_percent',
        ),
    ]