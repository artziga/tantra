import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.signing import Signer

signer = Signer()
logger = logging.getLogger(name='email_logger')
logger.setLevel(level=logging.DEBUG)


def send_activation_notification(user):
    """
    Отправляет уведомление об активации пользователя по электронной почте.
    """
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[-1] not in ['localhost', '127.0.0']:
        host = 'https://' + settings.ALLOWED_HOSTS[-1]
    else:
        host = 'localhost:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('accounts/activation_letter_subject.txt', context)
    body_text = render_to_string('accounts/activation_letter_body.html', context)
    try:
        email = EmailMessage(subject, body_text, to=[user.email])
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        logger.error(f'Ошибка отправки письма: {e}')
        raise e  # TODO: сделать через celery
