from django import forms
from django.contrib.auth import get_user_model

from gallery.forms import max_image_size_text

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    """
       Форма редактирования профиля пользователя.
    """

    avatar = forms.ImageField(label='Аватар', required=False, help_text=max_image_size_text,
                              widget=forms.ClearableFileInput())
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

