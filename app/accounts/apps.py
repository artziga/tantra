from django.apps import AppConfig
from django.dispatch import Signal

from accounts.utils import send_activation_notification


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


user_registered = Signal()


def user_registered_dispatcher(instance, **kwargs):
    send_activation_notification(instance)


user_registered.connect(user_registered_dispatcher)
