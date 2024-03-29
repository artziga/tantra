from django.contrib.auth import get_user_model
from django.db import models

from listings.models import Feature
from django.urls import reverse

from users.validators import validate_age


class BasicService(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Базовая услуга'
        verbose_name_plural = 'Базовые услуги'


class BasicServicePrice(models.Model):
    service = models.ForeignKey(BasicService,
                                on_delete=models.CASCADE,
                                )
    specialist = models.ForeignKey('specialists.SpecialistProfile', on_delete=models.CASCADE, null=True)
    home_price = models.PositiveSmallIntegerField(verbose_name='Приём у себя')
    on_site_price = models.PositiveSmallIntegerField(verbose_name='Выезд на дом', null=True, blank=True)


class MassageFor(models.Model):
    massage_for = models.CharField(max_length=50, verbose_name='Массаж для')
    slug = models.SlugField()
    icon = models.CharField(max_length=50, verbose_name='Иконка')

    def __str__(self):
        return self.massage_for

    class Meta:
        verbose_name = 'Для кого массаж'
        verbose_name_plural = verbose_name


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
    whatsapp_profile = models.CharField(max_length=20, verbose_name='Whatsapp', null=True, blank=True)
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
