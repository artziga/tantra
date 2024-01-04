from django.contrib.auth import models
from django.db.models import F, OuterRef, Subquery, ImageField, Prefetch, Count, Avg

from gallery.models import Photo
from feedback.models import Review


class SpecialistsManager(models.UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_specialist=True)

    def active(self):
        return self.filter(
            specialist_profile__is_profile_active=True)

    def specialist_card_info(self):
        avatar_photos = Prefetch('photos', queryset=Photo.objects.filter(is_avatar=True), to_attr='avatar')
        review = Prefetch('review_for', queryset=Review.objects.all(), to_attr='score')
        qs = (self.select_related('specialist_profile').prefetch_related(avatar_photos, review)
              .filter(specialist_profile__is_profile_active=True))

        qs = qs.annotate(
            min_price=F('specialist_profile__basicserviceprice__home_price'),
            # TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
            num_reviews=Count('review_for', distinct=True),
            avg_score=Avg('review_for__score')
        )

        return qs
