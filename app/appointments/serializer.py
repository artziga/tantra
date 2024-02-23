from rest_framework import serializers

from appointments.models import WorkSlots


class WorkSlotsSerializer(serializers.ModelSerializer):
    """Список доступных слотов"""
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = WorkSlots
        fields = ("id", "start_time", "end_time", "day_of_week", "day_of_week_display")
