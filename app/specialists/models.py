from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from star_ratings.models import Rating

from listings.models import MassageFor, Feature, BasicService
from django.urls import reverse


def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise ValidationError("Вам должно быть более 18 лет для регистрации", code='too_young')
    elif age >= 100:
        raise ValidationError("Введите корректный возраст", code='too_old')


class SpecialistProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,

        related_name='specialist_profile',
        related_query_name='specialist_profile'
    )
    gender = models.BooleanField(verbose_name='Пол', null=True, blank=True,
                                 choices=((True, 'Мужчина'), (False, 'Женщина')))
    massage_for = models.ManyToManyField(MassageFor, related_name='specialists', related_query_name='specialist')
    basic_services = models.ManyToManyField(BasicService, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    birth_date = models.DateField(verbose_name='Возраст', blank=True, null=True, validators=[validate_age])
    height = models.PositiveSmallIntegerField(verbose_name='Рост', null=True, blank=True)
    weight = models.PositiveSmallIntegerField(verbose_name='Вес', null=True, blank=True)
    practice_start_date = models.DateField(verbose_name='Дата начала практики', blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name='Адрес', null=True, blank=True)
    latitude = models.FloatField(verbose_name='широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='долгота', null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    telegram_profile = models.CharField(max_length=20, verbose_name='Телеграмм', null=True, blank=True)
    instagram_profile = models.CharField(max_length=20, verbose_name='Инстаграм', null=True, blank=True)
    description = models.TextField(verbose_name='О себе', null=True, blank=True)
    is_profile_active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('specialists:specialist_profile', kwargs={'specialist_username': self.user.username})

    def __str__(self):
        return self.user.username

    @property
    def gender_display(self):
        return 'Мужчина' if self.gender is True else 'Женщина'

    @property
    def point(self):
        return [self.latitude, self.longitude]

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
