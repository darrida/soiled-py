# Generated by Django 5.1.4 on 2024-12-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_feature_flags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='enable_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='remove_old_func',
            field=models.BooleanField(default=False, help_text='Feature change was successful and old code can be removed.', verbose_name='Remove old functionality'),
        ),
        migrations.AddField(
            model_name='feature',
            name='succeeded',
            field=models.BooleanField(default=False, help_text='Feature confirmed working.'),
        ),
    ]
