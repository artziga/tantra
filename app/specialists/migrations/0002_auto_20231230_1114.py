# Generated by Django 5.0 on 2023-12-30 08:14
from django.core.management import call_command
from django.db import migrations


def load_initial_data(apps, schema_editor):
    call_command('loaddata', 'specialists/fixtures/basic_service_initial.json', app_label='specialists')
    call_command('loaddata', 'specialists/fixtures/massage_for_initial.json', app_label='specialists')


class Migration(migrations.Migration):
    dependencies = [
        ('specialists', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
