from django.contrib.auth import models
from django.db.models import F, OuterRef, Subquery, ImageField, Prefetch

from gallery.models import Photo


class SpecialistsManager(models.UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_specialist=True)

    def active(self):
        return self.filter(
            specialist_profile__is_profile_active=True)

    def specialist_card_info(self):
        avatar_photos = Prefetch('photos', queryset=Photo.objects.filter(is_avatar=True), to_attr='avatar')
        rating = Prefetch('reviews', to_attr='review')
        qs = (self.select_related('specialist_profile').prefetch_related(avatar_photos, rating)
              .filter(specialist_profile__is_profile_active=True))

        qs = qs.annotate(
            min_price=F('specialist_profile__basicserviceprice__home_price'),
            # TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
        )

        return qs
