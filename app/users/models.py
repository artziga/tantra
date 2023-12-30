import logging

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from star_ratings.models import Rating

from feedback.models import Bookmark
from gallery.models import Photo
from users.managers import SpecialistsManager


class User(AbstractUser):
    is_verified = models.BooleanField(verbose_name='Подтверждён', default=False)
    is_specialist = models.BooleanField(verbose_name='Массажист', default=False)
    rating = GenericRelation(Rating, related_name='users', related_query_name='user')
    bookmarks = GenericRelation(Bookmark, related_name='users')
    reviews = GenericRelation(Rating, related_name='users')

    objects = UserManager()
    specialists = SpecialistsManager()

    def __str__(self):
        if self.first_name or self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.first_name or self.username

    @property
    def avatar(self):
        try:
            avatar = Photo.objects.get(user=self, is_avatar=True)
        except ObjectDoesNotExist:
            avatar = None
            logging.warning('Нет аватара')
        except MultipleObjectsReturned:
            logging.warning('Было более одного аватара')
            all_avatars = Photo.objects.filter(user=self, is_avatar=True)
            fake_avatars = list(all_avatars[1:])
            Photo.objects.filter(id__in=[avatar.id for avatar in fake_avatars]).update(is_avatar=False)
            avatar = all_avatars.first()

        return avatar
