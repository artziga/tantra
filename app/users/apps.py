from django.apps import AppConfig
from django.dispatch import Signal


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Мастера'

