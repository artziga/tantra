from django import template
from django.urls import reverse_lazy

from main.templatetags.menu import get_menu

register = template.Library()


@register.inclusion_tag('users/sidebar.html')
def sidebar(user, selected):
    user_menu = get_menu(user)
    return {
        'menu': user_menu,
        'current': selected
    }
