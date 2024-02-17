from django.contrib.auth import get_user_model
from rest_framework import serializers

from gallery.serializers import PhotoSerializer
from .models import Review
from .templatetags.rating_tags import rating_class
from .utils import get_reviews

User = get_user_model()


class ReviewUserSerializer(serializers.ModelSerializer):
    avatar_img = PhotoSerializer(source='avatar', read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar_img')


class ReviewSerializer(serializers.ModelSerializer):
    """Список отзывов"""
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    score = serializers.IntegerField()
    rating_class = serializers.SerializerMethodField()
    author = ReviewUserSerializer(read_only=True)
    is_current_user_author = serializers.SerializerMethodField()
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        exclude = ('user',)

    def get_rating_class(self, obj):
        return rating_class(obj.score)

    def get_is_current_user_author(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        return obj.author == user
