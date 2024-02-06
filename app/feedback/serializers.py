from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Список отзывов"""

    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ('user',)
