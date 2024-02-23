from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from appointments.serializer import WorkSlotsSerializer
from appointments.utils import get_specialists_work_slots
from specialists.models import SpecialistProfile

User = get_user_model()


class SlotsViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = WorkSlotsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_specialists_work_slots(self.kwargs['specialist_username'])

    def perform_create(self, serializer):
        specialist = self.kwargs['specialist_username']
        specialist = get_object_or_404(SpecialistProfile, user__username=specialist)
        serializer.save(specialist=specialist)
