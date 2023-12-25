from django import forms


class StarRatingWidget(forms.Widget):
    template_name = 'feedback/widgets/star_rating.html'
