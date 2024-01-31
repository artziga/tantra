from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView

from django.views.generic import CreateView, TemplateView


User = get_user_model()


class MyLoginView(LoginView):
    """
    Класс представления для отображения страницы входа пользователя.
    """


class RegisterUserView(CreateView):
    """
    Класс представления для регистрации обычного пользователя.
    """


class RegisterSpecialistView(RegisterUserView):
    """
    Класс представления для регистрации пользователя в роли специалиста.
    """


class RegistrationDone(TemplateView):
    """
    Класс представления для отображения страницы успешной регистрации.
    """


def user_activate(request, sign):
    """
    Функция для активации пользователя по подписанному токену.
    """


class MyPasswordChangeView(PasswordChangeView):
    """
    Класс представления для изменения пароля пользователя.
    """


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Класс представления для сброса пароля пользователя.
    """
