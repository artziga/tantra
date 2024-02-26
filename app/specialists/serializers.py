from django.contrib.auth import get_user_model
from rest_framework import serializers

from gallery.serializers import PhotoSerializer, PhotosSerializer
from specialists.models import SpecialistProfile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistProfile
        fields = (
            "gender",
            "birth_date",
            "practice_start_date",
            "address",
            "telegram_profile",
            "whatsapp_profile",
            "instagram_profile",
            "phone_number",
            "description",
            "features",
            "massage_for"
        )


class SpecialistSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    specialist_profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'specialist_profile', 'photos')
