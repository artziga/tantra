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
    bookmarks = GenericRelation(Bookmark, related_name='users')

    objects = UserManager()
    specialists = SpecialistsManager()

    def __str__(self):
        if self.first_name or self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return self.username

    @property
    def name(self):
        return self.first_name or self.username

    @property
    def avatar(self):
        try:
            avatar = Photo.objects.get(user=self, is_avatar=True)
        except ObjectDoesNotExist:
            return None
        return avatar
