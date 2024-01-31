from django import forms


class StarRatingWidget(forms.Widget):
    """
    Виджет поля ввода оценки в виде звёзд
    """
    template_name = 'feedback/widgets/star_rating.html'
