from django.core.exceptions import ValidationError


def validate_single_avatar(value):
    user = value.user
    if user.photos.filter(is_avatar=True).exclude(id=value.id).exists():
        raise ValidationError('У пользователя может быть только один аватар.', code='single_avatar')
