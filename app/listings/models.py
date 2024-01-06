from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Listing(models.Model):
    specialist = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='listings',
                                   related_query_name='listing',
                                   verbose_name='Массажист')
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True)
    duration = models.DurationField(verbose_name='Продолжительность')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name
