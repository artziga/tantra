from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from star_ratings.models import UserRating

from config import settings


class BaseComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name='автор',
                               related_query_name='review',
                               related_name='reviews')
    text = models.TextField(max_length=255, verbose_name='Отзыв')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Родительский комментарий',
        related_name='child_comment',
        related_query_name='child_comments')
    date_added = models.DateTimeField('Дата создания',
                                      auto_now_add=True)

    class Meta:
        abstract = True


class Review(models.Model):
    text = models.TextField(max_length=255, verbose_name='Отзыв')
    # score = models.OneToOneField(
    #     UserRating,
    #     verbose_name='Оценка',
    #     on_delete=models.CASCADE,
    #     related_name='review',
    #     related_query_name='review',
    # )


class Bookmark(models.Model):
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user.username
