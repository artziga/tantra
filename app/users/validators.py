from datetime import date

from django.core.exceptions import ValidationError


def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise ValidationError("Вам должно быть более 18 лет для регистрации", code='too_young')
    elif age >= 100:
        raise ValidationError("Введите корректный возраст", code='too_old')
