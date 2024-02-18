from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Value, BooleanField, Subquery

from feedback.models import Review, Bookmark
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


def add_is_bookmarked(queryset, user):
    """
        Добавляет атрибут is_bookmarked к queryset, указывающий,
        добавлен ли объект в избранное для конкретного пользователя.
    """

    if user and user.is_authenticated:
        bookmarked_subquery = Bookmark.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(User),
            object_id=OuterRef('pk')
        ).values('user').annotate(is_bookmarked=Value(True, output_field=BooleanField())).values('is_bookmarked')
        queryset = queryset.annotate(
            is_bookmarked=Subquery(bookmarked_subquery, output_field=BooleanField())
        )

    return queryset


def get_reviews(obj):
    return Review.objects.filter(user=obj)
