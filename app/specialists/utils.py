from email._header_value_parser import get_domain

from django.core.mail import send_mail

from gallery.models import Photo
from config.settings import DEFAULT_FROM_EMAIL
from specialists.models import SpecialistProfile


def make_user_a_specialist(user):
    user.is_specialist = True
    user.save()
    SpecialistProfile.objects.create(user=user)
    subject = 'Новый массажист ожидает подтверждения'
    count = SpecialistProfile.objects.filter(is_profile_active=False).count()
    message = (f'Зарегистрирован новый массажист.'
               f' Он ожидает подтверждения своего профиля.\nВсего профилей для подтверждения: {count}')
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = ['kazan-tantra@yandex.ru']

    send_mail(subject, message, from_email, recipient_list) #TODO: Надо сделать асинхронно


def delete_specialist(user):
    user.is_specialist = False
    user.save()
    specialist_profile = SpecialistProfile.objects.get(user=user)
    photos = Photo.objects.filter(user=user, is_avatar=False)
    photos.delete()
    specialist_profile.delete()
