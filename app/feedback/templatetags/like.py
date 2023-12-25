from django import template
from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()


@register.inclusion_tag('feedback/like_button.html')
def like_button(user_id, object_id, content_type_id, is_bookmarked):
    return {
        'user': User.objects.get(pk=user_id),
        'specialist': object_id,
        'content_type': content_type_id,
        'is_bookmarked': is_bookmarked
    }
