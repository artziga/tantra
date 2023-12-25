from datetime import timedelta

from django import forms

from listings.models import Listing


class CreateOfferForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form__input'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(
        attrs={'class': 'form__input form__input--textarea'}))
    price = forms.IntegerField(label='Цена, ₽', widget=forms.NumberInput(attrs={'class': 'form__input'}))
    hours = forms.IntegerField(label='ч.', widget=forms.NumberInput(attrs={'class': 'form__input w--50'}))
    minutes = forms.IntegerField(label='мин.', widget=forms.NumberInput(attrs={'class': 'form__input w--50'}))

    def clean(self):
        cleaned_data = super().clean()
        duration = self._clean_duration()
        self.cleaned_data['duration'] = duration
        return cleaned_data

    def _clean_duration(self):
        hours = self.cleaned_data.pop('hours')
        minutes = self.cleaned_data.pop('minutes')
        return timedelta(hours=hours, minutes=minutes)

    class Meta:
        model = Listing
        exclude = ['specialist', 'duration', 'tags']
        widgets = {}
