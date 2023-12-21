from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm, PasswordChangeForm, \
    SetPasswordForm

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form__input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form__input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form__input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'password')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form__input', "autocomplete": "email"}),
    )


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form__input'
        })

        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form__input'
        })


class MyPasswordChangeForm(MySetPasswordForm, PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form__input'}),
        label='Текущий пароль'
    )




