from django.contrib.auth import get_user_model
from rest_framework import serializers

from gallery.serializers import PhotoSerializer
from .models import Review
from .templatetags.rating_tags import rating_class

User = get_user_model()


class ReviewUserSerializer(serializers.ModelSerializer):
    avatar_img = PhotoSerializer(source='avatar', read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar_img')


class ReviewSerializer(serializers.ModelSerializer):
    """Список отзывов"""
    author = ReviewUserSerializer(read_only=True)
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    rating_class = serializers.SerializerMethodField()


    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('user', 'score')
    def get_rating_class(self, obj):
        return rating_class(obj.score)
