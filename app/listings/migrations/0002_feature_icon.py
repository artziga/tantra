# Generated by Django 5.0 on 2024-01-06 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='icon',
            field=models.CharField(max_length=50, null=True, verbose_name='Иконка'),
        ),
    ]
