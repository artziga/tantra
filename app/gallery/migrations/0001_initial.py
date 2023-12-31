# Generated by Django 5.0 on 2023-12-24 12:50

import autoslug.fields
import django.db.models.deletion
import gallery.models
import imagekit.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=gallery.models.get_storage_path, verbose_name='фото')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=gallery.models.BaseImage.generate_slug, unique=True, verbose_name='слаг')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_avatar', models.BooleanField(default=False, verbose_name='Аватар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', related_query_name='photo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'фото',
                'ordering': ['-is_avatar', '-upload_date', '-pk'],
                'get_latest_by': 'upload_date',
            },
        ),
    ]
