# from django.contrib import admin
# from star_ratings import get_star_ratings_rating_model
# from star_ratings.admin import RatingAdmin, UserRatingAdmin
# from star_ratings.models import UserRating
# from feedback.models import Review
# from django.apps import apps

# admin.site.unregister(apps.get_model('star_ratings', 'Rating'))
# admin.site.unregister(apps.get_model('star_ratings', 'UserRating'))


# class UserRatingAdminModel(UserRating):
#     class Meta:
#         proxy = True
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'
#
#
# class RatingModelAdmin(RatingAdmin):
#     pass
#
#
# class ReviewInline(admin.StackedInline):  # Или используйте admin.TabularInline, в зависимости от ваших предпочтений
#     model = Review
#     extra = 1
#
#
# class UserReviewAdmin(UserRatingAdmin):
#     inlines = [ReviewInline]
#     list_display = ('__str__', 'get_review_text', 'stars')
#
#     def get_review_text(self, obj):
#         return obj.review.text if obj.review else None
#
#     get_review_text.short_description = 'Текст отзыва'


# admin.site.register(get_star_ratings_rating_model(), RatingModelAdmin)
# admin.site.register(UserRatingAdminModel, UserReviewAdmin)
