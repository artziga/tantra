import os

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import SmartResize, Thumbnail

User = get_user_model()


def get_storage_path(instance, filename: str) -> str:
    title = instance.title
    author = instance.author
    path = os.path.join('articles', author, title, filename)
    return path


class BaseArticle(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = AutoSlugField(db_index=True, unique=True, populate_from='title')
    body = RichTextField(verbose_name='Текст')
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    date_added = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        editable=False
    )
    date_modified = models.DateTimeField(verbose_name='Дата изменения', auto_now=True, null=True, blank=True)

    thumbnail = ImageSpecField(source='image',
                               processors=[Thumbnail(100, 100)
                                           ],
                               format='JPEG',
                               options={'quality': 100})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Article(BaseArticle):
    image_size = (800, 561)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор',
        related_query_name='article'
    )

    image = ProcessedImageField(verbose_name='фото',
                                processors=[SmartResize(*image_size)],
                                max_length=100,
                                upload_to='articles/%Y/%m',
                                )

    card_thumbnail = ImageSpecField(source='image',
                                    processors=[Thumbnail(400, 280)
                                                ],
                                    format='JPEG',
                                    options={'quality': 100})

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_added']
        get_latest_by = 'date_added'


class Announcement(BaseArticle):
    image_size = (800, 561)
    place = models.CharField(max_length=100, null=True, blank=True, verbose_name='Место',
                             help_text='Место проведения')
    event_time = models.DateTimeField(verbose_name='Дата и время мероприятия', null=True, blank=True, )
    image = ProcessedImageField(verbose_name='фото',
                                processors=[SmartResize(*image_size)],
                                max_length=100,
                                upload_to='articles/%Y/%m',
                                )

    card_thumbnail = ImageSpecField(source='image',
                                    processors=[Thumbnail(444, 567)
                                                ],
                                    format='JPEG',
                                    options={'quality': 100})

    def get_absolute_url(self):
        return reverse('articles:announcement_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Анонс'
        verbose_name_plural = 'Анонсы'
        ordering = ['-event_time']
        get_latest_by = 'event_time'
