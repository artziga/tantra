import os

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import SmartResize

User = get_user_model()



def get_storage_path(instance, filename: str) -> str:
    title = instance.title
    author = instance.author
    path = os.path.join('articles', author, title, filename)
    return path


class BaseArticle(models.Model):


    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = AutoSlugField(db_index=True, unique=True, populate_from='title')
    body = models.TextField(verbose_name='Текст')
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    date_added = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        editable=False
    )
    date_modified = models.DateTimeField(verbose_name='Дата изменения', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Article(BaseArticle):
    image_size = (444, 567)
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

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_added']
        get_latest_by = 'date_added'


class Announcement(BaseArticle):
    image_size = (500, 466)
    place = models.CharField(max_length=100, null=True, blank=True, verbose_name='Место',
                             help_text='Место проведения')
    event_time = models.DateTimeField(verbose_name='Дата и время мероприятия', null=True, blank=True, )
    image = ProcessedImageField(verbose_name='фото',
                                processors=[SmartResize(*image_size)],
                                max_length=100,
                                upload_to='articles/%Y/%m',
                                )

    class Meta:
        verbose_name = 'Анонс'
        verbose_name_plural = 'Анонсы'
        ordering = ['-event_time']
        get_latest_by = 'event_time'
