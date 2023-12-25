from django import forms
from feedback.widgets import StarRatingWidget


class ReviewForm(forms.Form):

    text = forms.CharField(label='Отзыв', widget=forms.Textarea(
                attrs={'class': 'form__input form__input--textarea', 'placeholder': 'Оставьте отзыв'}))
    review_for = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    score = forms.IntegerField(label='Оценка', required=True, widget=StarRatingWidget())


