from django import forms


class ContactUsForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'email'}))
    name = forms.CharField(label='Имя', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Ваше имя'}))
    text = forms.CharField(label='Сообщение', widget=forms.Textarea(
        attrs={'class': 'form__input form__input--textarea', 'placeholder': 'Ваше сообщение'}))
