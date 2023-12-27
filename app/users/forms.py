from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EditProfileForm(forms.ModelForm):

    avatar = forms.ImageField(label='Аватар', required=False, widget=forms.ClearableFileInput())
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

