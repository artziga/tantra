from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BaseComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_query_name='review',
                               related_name='reviews')
    text = models.TextField(max_length=255, verbose_name='Комментарий')
    date_added = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        null=True
    )

    class Meta:
        abstract = True


class Review(BaseComment):
    score = models.SmallIntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Кому',
        related_name='review_for')

    class Meta:
        unique_together = ('user', 'author')


# class Comment(BaseComment):
#     parent = models.ForeignKey(
#         'self',
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         verbose_name='Родительский комментарий',
#         related_name='child_comment',
#         related_query_name='child_comments')


class Bookmark(models.Model):
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user.username
