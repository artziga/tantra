from datetime import timedelta

from django import forms


from listings.models import Listing


class CreateOfferForm(forms.ModelForm):
    # tags = TagField(
    #     required=False,
    #     widget=autocomplete.TaggitSelect2('tag_autocomplete', attrs={'placeholder': 'Вводите тэги через запятую'})
    # )
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form__input'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(
        attrs={'class': 'form__input form__input--textarea'}))
    price = forms.IntegerField(label='Цена, ₽', widget=forms.NumberInput(attrs={'class': 'form__input'}))
    hours = forms.IntegerField(label='ч.', widget=forms.NumberInput(attrs={'class': 'form__input w--50'}))
    minutes = forms.IntegerField(label='мин.', widget=forms.NumberInput(attrs={'class': 'form__input w--50'}))

    def clean(self):
        cleaned_data = super().clean()
        # tags = self._clean_tags()
        # cleaned_data['tags'] = tags
        duration = self._clean_duration()
        self.cleaned_data['duration'] = duration
        return cleaned_data
    #
    # def _clean_tags(self):
    #     print(self.cleaned_data['tags'])
    #     tags_names = set(tag.strip() for tag in self.cleaned_data['tags'].split(','))
    #     tags = set()
    #     for tag_name in tags_names:
    #         tag, created = Tag.objects.get_or_create(tag_name=tag_name)
    #         tags.add(tag)
    #     return tags

    def _clean_duration(self):
        hours = self.cleaned_data.pop('hours')
        minutes = self.cleaned_data.pop('minutes')
        return timedelta(hours=hours, minutes=minutes)

    class Meta:
        model = Listing
        exclude = ['specialist', 'duration', 'tags']
        widgets = {}
