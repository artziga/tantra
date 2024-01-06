from django.core.exceptions import ValidationError


def validate_single_avatar(value):
    user = value.user
    if user.photos.filter(is_avatar=True).exclude(id=value.id).exists():
        raise ValidationError('У пользователя может быть только один аватар.', code='single_avatar')

# def avatar(user):
#     try:
#         avatar = Photo.objects.get(user=self, is_avatar=True)
#     except ObjectDoesNotExist:
#         avatar = None
#         logging.warning('Нет аватара')
#     except MultipleObjectsReturned:
#         logging.warning('Было более одного аватара')
#         all_avatars = Photo.objects.filter(user=self, is_avatar=True)
#         fake_avatars = list(all_avatars[1:])
#         Photo.objects.filter(id__in=[avatar.id for avatar in fake_avatars]).update(is_avatar=False)
#         avatar = all_avatars.first()
#
#     return avatar
