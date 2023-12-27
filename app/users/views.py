from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from django.db.models import F, OuterRef, Value, BooleanField, Subquery
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, UpdateView
import logging

from accounts.views import MyPasswordChangeView
from feedback.models import Bookmark
from feedback.views import add_is_bookmarked
from gallery.forms import AvatarForm
from gallery.views import add_avatar
from users.forms import EditProfileForm
from users.models import *

from config.utils import DataMixin
from gallery.models import Photo

User = get_user_model()


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = Photo
    form_class = AvatarForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление фото пользователя')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        image = self.request.FILES.get('avatar')
        if image:
            user = self.request.user
            photo, created = Photo.objects.get_or_create(is_avatar=True, user=user)
            photo.image = image
            photo.save()
        return super().form_valid(form)


class ProfileView(DataMixin, TemplateView):
    template_name = 'users/profile_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        context['selected'] = self.request.user.username
        return {**context, **context_def}


class Favorite(ListView):
    context_object_name = 'favorite_specialists'
    template_name = 'users/profile_favorite.html'

    def get_queryset(self):
        specialists = User.specialists.specialist_card_info()
        specialists = add_is_bookmarked(queryset=specialists, user=self.request.user)
        ct = ContentType.objects.get_for_model(User)
        favorite_specialists_pk = (Bookmark.objects.
                                   filter(content_type=ct, user=self.request.user).values_list('object_id', flat=True))
        favorite_specialists = specialists.filter(pk__in=favorite_specialists_pk)
        return favorite_specialists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Избранное'
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        return context


class EditProfile(UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        username = self.kwargs.get('username')
        if not username:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        queryset = queryset.filter(username=username)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def form_valid(self, form):
        add_avatar(user=self.request.user, form=form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Редактировать профиль'
        return context


class UserPasswordChangeView(MyPasswordChangeView):
    template_name = 'users/profile_change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Сменить пароль'
        return context
