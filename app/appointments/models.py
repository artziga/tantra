from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from specialists.models import SpecialistProfile

User = get_user_model()


class BaseWorkSlots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        abstract = True


class WorkSlots(BaseWorkSlots):
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name="slots")
    day_of_week = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])

    class Meta:
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"


class Appointments(BaseWorkSlots):
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name="specialists_appointments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_appointments")
    comment = models.TextField(max_length=255, verbose_name='Комментарий')

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
