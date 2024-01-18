from django.conf import settings
from django.core.exceptions import FieldError
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import render_to_string

from gallery.models import Photo
from specialists.models import SpecialistProfile


def make_user_a_specialist(user):
    user.is_specialist = True
    user.save()
    specialist = SpecialistProfile.objects.create(user=user)
    subject = 'Новый массажист ожидает подтверждения'
    count = SpecialistProfile.objects.filter(is_profile_active=False).count()
    model_name = specialist._meta.model_name
    app_label = specialist._meta.app_label
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[-1] not in ['localhost', '127.0.0']:
        host = 'http://' + settings.ALLOWED_HOSTS[-1]
    else:
        host = 'localhost:8000'
    specialists_url = f'{host}/admin/{app_label}/{model_name}'
    specialist_url = f'{host}/admin/{app_label}/{model_name}/{specialist.pk}/change'
    context = {
        'specialist': specialist,
        'count': count,
        'specialists_url': specialists_url,
        'specialist_url': specialist_url,
    }
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['kazan-tantra@yandex.ru']
    html_content = render_to_string('specialists/specialist_activation_for_admin.html', context)
    email = EmailMessage(subject, html_content, to=recipient_list, from_email=from_email)
    email.content_subtype = 'html'
    email.send()  # TODO: Надо сделать асинхронно


def delete_specialist(user):
    user.is_specialist = False
    user.save()
    specialist_profile = SpecialistProfile.objects.get(user=user)
    photos = Photo.objects.filter(user=user, is_avatar=False)
    photos.delete()
    specialist_profile.delete()


price_range = {'low': (6000, 11000), 'medium': (11000, 15000), 'high': (15000, 20000)}


def filter_specialists(queryset, parameters, for_map=False):
    genders = parameters.getlist('gender') or [True, False]
    massage_for = ([mf.slug for mf in parameters.getlist('massage_for', [])]
                   or ['for_males', 'for_females', 'for_pairs'])
    price = parameters.get('price', None)
    queryset = (queryset.
                filter(
        specialist_profile__gender__in=genders,
        specialist_profile__massage_for__slug__in=massage_for
    )
                .distinct())
    if not for_map:
        if price:
            price_filter = Q(min_price__gte=price_range[price][0], min_price__lte=price_range[price][1])
            queryset = queryset.filter(price_filter)
        ordering = parameters.get('order_by')

        if ordering:
            queryset = queryset.order_by(ordering)

    return queryset
