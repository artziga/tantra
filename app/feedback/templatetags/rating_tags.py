from django import template
from config import settings

register = template.Library()


@register.inclusion_tag('feedback/star_rating.html')
def rating(rat):
    if rat:
        half_star = False
        rounded_rating = round(rat * 2) / 2
        int_rating = int(rounded_rating)
        full_stars = range(int_rating)
        empty_stars_count = 5 - int_rating
        if not rounded_rating.is_integer():
            half_star = True
            empty_stars_count -= 1
        empty_stars = range(empty_stars_count)
        return {'stars': full_stars,
                'half_star': half_star,
                'o_stars': empty_stars
                }


@register.simple_tag()
def rating_class(rat):
    ratings = {
        0.5: 'star-half',
        1: 'star-one',
        1.5: 'star-one-half',
        2: 'star-two',
        2.5: 'star-two-half',
        3: 'star-three',
        3.5: 'star-three-half',
        4: 'star-four',
        4.5: 'star-four-half',
        5: 'star-five',
    }
    if rat:
        rounded_rating = round(rat * 2) / 2
        return ratings[rounded_rating]
    else:
        return 'star-null'
