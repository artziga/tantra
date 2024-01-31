from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordResetForm, UserCreationForm, PasswordChangeForm, SetPasswordForm
)

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    Добавляет дополнительное поле 'is_adult', чтобы подтвердить совершеннолетие пользователя.
    """

    is_adult = forms.BooleanField(label='Мне больше 18 лет', widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_adult')


class LoginUserForm(AuthenticationForm):
    """
    Форма аутентификации пользователя.
    Используется для входа пользователя в систему.
    """

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'password')


class UserPasswordResetForm(PasswordResetForm):
    """
    Форма сброса пароля пользователя.
    Используется для отправки электронного письма со ссылкой на сброс пароля.
    """

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form__input', "autocomplete": "email"}),
    )


class MySetPasswordForm(SetPasswordForm):
    """
    Форма установки нового пароля пользователя.
    Используется для установки нового пароля после сброса.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form__input'
        })

        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form__input'
        })


class MyPasswordChangeForm(MySetPasswordForm, PasswordChangeForm):
    """
    Форма изменения пароля пользователя.
    Используется для изменения пароля пользователя.
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form__input'}),
        label='Текущий пароль'
    )
