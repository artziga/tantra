# Generated by Django 5.0 on 2024-01-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specialists', '0003_specialistprofile_whatsapp_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicserviceprice',
            name='home_price',
            field=models.PositiveSmallIntegerField(verbose_name='Приём у себя'),
        ),
    ]
