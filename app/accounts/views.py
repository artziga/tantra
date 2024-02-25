from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.apps import user_registered
from accounts.forms import LoginUserForm, RegisterUserForm, MyPasswordChangeForm, MySetPasswordForm
from accounts.utils import signer
from specialists.utils import make_user_a_specialist

User = get_user_model()


class MyLoginView(LoginView):
    """
    Класс представления для отображения страницы входа пользователя.
    """

    template_name = "accounts/login.html"
    form_class = LoginUserForm
    extra_context = {'title': 'Вход', 'button_label': 'Вход'}

    def get_success_url(self):
        return reverse_lazy('specialists:profile') if self.request.user.is_specialist else reverse_lazy('users:profile')


class RegisterUserView(CreateView):
    """
        Класс представления для регистрации обычного пользователя.
    """

    model = User
    form_class = RegisterUserForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:registration_done')
    extra_context = {'tile': 'Регистрация'}

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user_registered.send(sender=self.__class__, instance=user)
        return response


class RegisterSpecialistView(RegisterUserView):
    """
        Класс представления для регистрации пользователя в роли специалиста.
    """

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        make_user_a_specialist(user)
        return response


class RegistrationDone(TemplateView):
    """
        Класс представления для отображения страницы успешной регистрации.

    """

    template_name = 'accounts/registration_done.html'
    extra_context = {'tile': 'Регистрация'}


def user_activate(request, sign):
    """
        Функция для активации пользователя по подписанному токену.
    """

    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html', {'title': 'Активация не удалась'})

    user = get_object_or_404(User, username=username)
    if user.is_verified:
        template = 'accounts/user_is_activated.html'
        return render(request, template, {'title': 'Активация выполнена ранее'})

    user.is_verified = True
    user.save()
    login(request, user)
    goto = 'users:edit_profile' if user.is_specialist else 'users:profile'
    return redirect(goto)


class MyPasswordChangeView(PasswordChangeView):
    """
    Класс представления для изменения пароля пользователя.
     """

    success_url = reverse_lazy("accounts:password_change_done")
    form_class = MyPasswordChangeForm


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Класс представления для сброса пароля пользователя.
    """

    template_name = 'accounts/password_reset_confirm.html'
    form_class = MySetPasswordForm
    post_reset_login = True
    success_url = reverse_lazy("users:profile")


def profile_view(request):
    if request.user.is_specialist:
        return redirect("specialists:profile")
    return redirect("users:profile")
