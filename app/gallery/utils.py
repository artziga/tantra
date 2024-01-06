from django.core.exceptions import MultipleObjectsReturned

from gallery.models import Photo


def make_single_avatar(user):
    all_avatars = Photo.objects.filter(user=user, is_avatar=True)
    fake_avatars = list(all_avatars[1:])
    Photo.objects.filter(id__in=[avatar.id for avatar in fake_avatars]).update(is_avatar=False)


def get_users_avatar(user):
    try:
        avatar = Photo.objects.get(user=user, is_avatar=True)
    except MultipleObjectsReturned:
        make_single_avatar(user)
        avatar = Photo.objects.get(user=user, is_avatar=True)
    return avatar


def make_as_avatar(photo):
    current_avatar = get_users_avatar(photo.user)
    if current_avatar:
        current_avatar.is_avatar = False
        current_avatar.save()
    photo.is_avatar = True
    photo.thumbnail.generate()
    photo.save()
