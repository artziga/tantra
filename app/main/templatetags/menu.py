from django import template
from django.urls import reverse_lazy

register = template.Library()


def get_menu(user):
    if user.is_specialist:
        menu = {
            user.username: reverse_lazy('specialists:profile'),
            'Редактировать профиль': reverse_lazy('specialists:edit_profile', kwargs={'username': user.username}),
            'Сменить пароль': reverse_lazy('specialists:change_password'),
            'Выйти': reverse_lazy('accounts:logout')
        }
    else:
        menu = {
            user.username: reverse_lazy('users:profile'),
            'Избранное': reverse_lazy('users:favorite'),
            'Редактировать профиль': reverse_lazy('users:edit_profile', kwargs={'username': user.username}),
            'Сменить пароль': reverse_lazy('users:change_password'),
            'Выйти': reverse_lazy('accounts:logout')
        }
    return menu


@register.inclusion_tag('main/profile_menu.html')
def profile_menu(user):
    if user.is_authenticated:
        menu = get_menu(user)
        return {'menu': menu, 'user': user}


@register.inclusion_tag('main/side_profile_menu.html')
def side_profile_menu(user):
    if user.is_authenticated:
        menu = get_menu(user)
        return {'menu': menu, 'user': user}
