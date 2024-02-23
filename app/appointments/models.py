from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q

from specialists.models import SpecialistProfile

User = get_user_model()


class BaseWorkSlots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        abstract = True


class WorkSlots(BaseWorkSlots):
    DAY_OF_WEEK_CHOICES = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name="slots")
    day_of_week = models.SmallIntegerField(choices=DAY_OF_WEEK_CHOICES,
                                           validators=[MinValueValidator(0), MaxValueValidator(6)])

    def clean(self):
        errors = {}
        if self.start_time is None or self.end_time is None:
            raise ValidationError("Заполните время начала и и окончания слота")
        specialist = self.specialist
        new_slot_start_time = self.start_time
        new_slot_end_time = self.end_time
        overlapping_events = WorkSlots.objects.filter(
            Q(start_time__lte=new_slot_start_time, end_time__gte=new_slot_start_time) |
            Q(start_time__lte=new_slot_end_time, end_time__gte=new_slot_end_time) |
            Q(start_time__gte=new_slot_start_time, end_time__lte=new_slot_end_time),
            day_of_week=self.day_of_week,
            specialist=specialist
        )
        if overlapping_events.exists():
            errors['start_time'] = ValidationError("Временные слоты не могут пересекаться")
        if new_slot_start_time > new_slot_end_time:
            errors['end_time'] = ValidationError("Время начала слота должно быть меньше времени его окончания")

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"


class Appointments(BaseWorkSlots):
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name="specialists_appointments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_appointments")
    comment = models.TextField(max_length=255, verbose_name='Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
