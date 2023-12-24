import logging
import os
import random
from io import BytesIO
from datetime import datetime

from PIL import Image
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail, SmartResize, ResizeCanvas

from config.settings import AUTH_USER_MODEL as User
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str, filepath_to_uri, smart_str
from django.utils.safestring import mark_safe

from gallery.photo_processor import CropFaceProcessor, get_square_borders

from config.settings import MEDIA_ROOT


LATEST_LIMIT = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', None)
SAMPLE_SIZE = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', 3)
IMAGE_FIELD_MAX_LENGTH = getattr(settings, 'PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH', 100)
#
CROP_ANCHOR_CHOICES = (
    ('top', 'Top'),
    ('right', 'Right'),
    ('bottom', 'Bottom'),
    ('left', 'Left'),
    ('center', 'Center (Default)'),
)
#
logger = logging.getLogger('gallery.models')

IMAGE_DIR = 'img/'
IMAGE_DIR_FOR_THUMB = 'media/img/'


def get_storage_path(instance, filename: str) -> str:
    user = instance.user.username
    path = os.path.join(IMAGE_DIR, user, filename)
    logger.info(f'{filename} сохранится в {path}')
    return path


class BaseImage(models.Model):
    image_size = (540, 600)

    def generate_slug(self):
        if self.image:
            image_name, ext = os.path.splitext(self.image.name)
            return image_name
        else:
            return 'no-name'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
        related_query_name='photo'
    )
    image = ProcessedImageField(verbose_name='фото',
                                processors=[SmartResize(*image_size)],
                                max_length=IMAGE_FIELD_MAX_LENGTH,
                                upload_to=get_storage_path,
                                )
    slug = AutoSlugField(verbose_name='слаг', db_index=True, unique=True, populate_from=generate_slug)
    admin_thumbnail = ImageSpecField(source='image',
                                     processors=[Thumbnail(100, 100)
                                                 ],
                                     format='JPEG',
                                     options={'quality': 60})
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Photo(BaseImage):
    is_avatar = models.BooleanField(verbose_name='Аватар', default=False)
    comment_thumbnail = ImageSpecField(source='image',
                                       processors=[CropFaceProcessor(margin_percent=0.6),
                                                   Thumbnail(90, 90)],
                                       format='JPEG',
                                       options={'quality': 90})
    mini_thumbnail = ImageSpecField(source='comment_thumbnail',
                                    processors=[Thumbnail(50, 50)],
                                    format='JPEG',
                                    options={'quality': 90})

    def make_as_avatar(self):
        current_avatar = self.user.avatar
        if current_avatar:
            current_avatar.is_avatar = False
            current_avatar.save()
        self.is_avatar = True
        self.mini_thumbnail.generate()
        self.comment_thumbnail.generate()
        self.save()

    class Meta:
        ordering = ['-is_avatar', '-upload_date', '-pk']
        get_latest_by = 'upload_date'
        verbose_name = 'фото'
