from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def format_duration(duration):
    # Проверяем, что значение duration является DurationField
    if isinstance(duration, timedelta):
        # Форматируем длительность в желаемом формате (например, HH:MM)
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02d} ч. {minutes:02d}м."
    else:
        # Возвращаем пустую строку или другое значение по умолчанию, если duration не является длительностью времени
        return ""
