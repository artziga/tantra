import logging
import os

from autoslug import AutoSlugField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, SmartResize

from config.settings import AUTH_USER_MODEL as User
from django.db import models

from gallery.validators import validate_single_avatar

CROP_ANCHOR_CHOICES = (
    ('top', 'Top'),
    ('right', 'Right'),
    ('bottom', 'Bottom'),
    ('left', 'Left'),
    ('center', 'Center (Default)'),
)
#
logger = logging.getLogger('gallery.models')

IMAGE_DIR = 'users_images/'
CACHE_DIR = 'CACHE/'


def get_storage_path(instance, filename: str) -> str:
    user = instance.user.username
    path = os.path.join(IMAGE_DIR, user, filename)
    logger.info(f'{filename} сохранится в {path}')
    return path


class BaseImage(models.Model):
    image_size = (1080, 1200)

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
                                max_length=100,
                                upload_to=get_storage_path,
                                )
    slug = AutoSlugField(verbose_name='слаг', db_index=True, unique=True, populate_from=generate_slug)
    thumbnail = ImageSpecField(source='image',
                               processors=[Thumbnail(100, 100)
                                           ],
                               format='JPEG',
                               options={'quality': 100})
    card_thumbnail = ImageSpecField(source='image',
                                    processors=[Thumbnail(270, 300)
                                                ],
                                    format='JPEG',
                                    options={'quality': 100})
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Photo(BaseImage):
    is_avatar = models.BooleanField(verbose_name='Аватар', default=False)

    def save(self, *args, **kwargs):
        current_avatar = Photo.objects.filter(user=self.user, is_avatar=True)
        if not current_avatar.exists():
            self.is_avatar = True
            self.thumbnail.generate()
            self.card_thumbnail.generate()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_avatar', '-upload_date', '-pk']
        get_latest_by = 'upload_date'
        verbose_name = 'фото'
