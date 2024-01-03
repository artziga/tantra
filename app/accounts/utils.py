import logging

from django.template.loader import render_to_string
from django.core.signing import Signer

from config.settings import ALLOWED_HOSTS

signer = Signer()
logger = logging.getLogger(name='email_logger')
logger.setLevel(level=logging.DEBUG)


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[-1]
    else:
        host = 'localhost:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('accounts/activation_letter_subject.txt', context)
    body_text = render_to_string('accounts/activation_letter_body.txt', context)
    try:
        user.email_user(subject, body_text)
    except Exception as e:
        logger.error(f'ошибка отправки письма: {e}')
        raise e  # TODO: сделать через celery
