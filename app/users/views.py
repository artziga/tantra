import logging
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, FormView
from formtools.wizard.views import SessionWizardView
from star_ratings.models import UserRating

from accounts.views import MyPasswordChangeView
from config import settings
from feedback.views import add_is_bookmarked
from gallery.forms import AvatarForm
from gallery.models import Photo
from gallery.views import add_avatar
from main.utils import FilterFormMixin
from users.forms import EditProfileForm, PersonDataForm, SpecialistDataForm, ContactDataForm, AboutForm, \
    SpecialistFilterForm
from users.mixins import SpecialistOnlyMixin
from users.models import SpecialistProfile, BasicService, BasicServicePrice
from users.utils import make_user_a_specialist, delete_specialist
from users.wrappers import specialist_only

User = get_user_model()


class AddAvatar(LoginRequiredMixin, FormView):
    model = Photo
    form_class = AvatarForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Добавление фото пользователя'}

    def form_valid(self, form):
        image = self.request.FILES.get('avatar')
        if image:
            user = self.request.user
            photo, created = Photo.objects.get_or_create(is_avatar=True, user=user)
            photo.image = image
            photo.save()
        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = 'users/profile_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['selected'] = self.request.user.username
        return context


# class Favorite(ListView):
#     context_object_name = 'favorite_specialists'
#     template_name = 'users/profile_favorite.html'
#     extra_context = {'selected': 'Избранное', 'content_type_id': ContentType.objects.get_for_model(User).pk}
#
#     def get_queryset(self):
#         specialists = User.specialists.specialist_card_info()
#         specialists = add_is_bookmarked(queryset=specialists, user=self.request.user)
#         ct = ContentType.objects.get_for_model(User)
#         favorite_specialists_pk = (Bookmark.objects.
#                                    filter(content_type=ct, user=self.request.user).values_list('object_id', flat=True))
#         favorite_specialists = specialists.filter(pk__in=favorite_specialists_pk)
#         return favorite_specialists


class EditProfile(UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('users:profile')
    extra_context = {'selected': 'Редактировать профиль'}

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


class UserPasswordChangeView(MyPasswordChangeView):
    template_name = 'users/profile_change_password.html'
    extra_context = {'selected': 'Сменить пароль'}


FORMS = [
    ('avatar', AvatarForm),
    ("person_data", PersonDataForm),
    ("specialist_data", SpecialistDataForm),
    ("contact_data", ContactDataForm),
    ("about", AboutForm),

]
FORMS_NAMES = [
    '<i class="fa-li fa fa-id-badge"></i>',
    '<i class="fa-li fa fa-address-card-o" aria-hidden="true"></i>',
    '<i class="fa-li fa fa-leaf" aria-hidden="true"></i>',
    '<i class="fa-li fa fa-phone-square" aria-hidden="true"></i>',
    '<i class="fa-li fa fa-file-text-o" aria-hidden="true"></i>'
]

TEMPLATES = {'avatar': 'forms/wizard_form_avatar.html'}


def become_a_specialist(request):
    return render(request, template_name='specialists/become_a_specialist_confirmation.html')


@specialist_only
def delete_specialist_profile(request):
    return render(request, template_name='specialists/delete_specialist_profile.html')


@specialist_only
def delete_a_specialist_confirmation(request):
    user = request.user
    delete_specialist(user)
    return redirect('users:profile')


class SpecialistProfileWizard(SessionWizardView):
    form_list = FORMS
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def get_form_kwargs(self, step=None):
        return {'user': self.request.user}

    # def process_step(self, form):
    #     if self.steps.current == 'contact_data':
    #         form.clean_address_data(user=self.request.user)
    #     return super().process_step(form)

    def get_template_names(self):
        return TEMPLATES.get(self.steps.current, 'forms/wizard_form.html')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        context['steps'] = FORMS_NAMES
        context['not_delete'] = True
        return dict(list(context.items()) + list(context_def.items()))

    def get_form_step_files(self, form):
        if self.steps.current == 'avatar':
            add_avatar(form, self.request.user, get='avatar-avatar')
        return super().get_form_step_files(form)

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        user = self.request.user
        user.first_name = cleaned_data.pop('first_name', '')
        user.last_name = cleaned_data.pop('last_name', '')
        massage_for_set = cleaned_data.pop('massage_for', [])
        cleaned_data.pop('avatar')
        home_price = cleaned_data.pop('home_price', '')
        on_site_price = cleaned_data.pop('on_site_price', '')
        if not user.is_specialist:
            make_user_a_specialist(user)
        tp, created = SpecialistProfile.objects.update_or_create(user=user, defaults=cleaned_data)
        self.set_price({
            'home_price': home_price,
            'on_site_price': on_site_price
        })
        tp.massage_for.set(massage_for_set)
        user.save()
        tp.save()
        logging.info(f"Заполнена анкета пользователем {user}")
        return redirect('gallery:edit_gallery')

    def set_price(self, data):
        bs = BasicService.objects.get(pk=1)
        BasicServicePrice.objects.update_or_create(
            service=bs,
            specialist=SpecialistProfile.objects.get(user=self.request.user),
            home_price=data['home_price'],
            on_site_price=data['on_site_price']
        )

    def get_form_initial(self, step):
        if self.request.user.is_specialist:
            forms = dict(FORMS)
            form = forms[step]
            initial = form.get_initial(self.request.user)

            return initial


class SpecialistProfileDetailView(ProfileView):
    template_name = 'specialists/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = self.get_user_context(**kwargs)
        specialist = self.get_specialist()
        # offers = Listing.objects.filter(specialist_id=specialist.pk)
        photos = Photo.objects.filter(user=specialist)
        ct = ContentType.objects.get_for_model(specialist)
        reviews = UserRating.objects.filter(rating__content_type=ct, rating__object_id=specialist.pk)
        is_reviewed = self.request.user in [review.user for review in reviews]
        review_form = self.get_review_form(specialist=specialist)
        context['is_reviewed'] = is_reviewed
        context['specialist'] = specialist
        context['content_type_id'] = ct.pk
        # context['offers'] = offers
        context['all_photos'] = photos
        # context['count'] = Bookmark.objects.filter(object_id=specialist.pk, content_type_id=ct.pk).count()
        # context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=ct.pk,
        #                                                    user_id=self.request.user.pk,
        #                                                    object_id=specialist.pk).exists()
        context['reviews'] = reviews
        context['form'] = review_form
        context['listings'] = specialist.listings.all()
        return context

    def get_specialist(self):
        specialist_name = self.kwargs.get('specialist_username')
        specialist = get_object_or_404(User, username=specialist_name)
        # specialist = User.objects.get(username=specialist_name)
        return specialist

    @staticmethod
    def get_review_form(specialist):
        # review_form = ReviewForm()
        # review_form.fields['review_for'].initial = specialist.pk
        review_form = 1
        return review_form


class SpecialistSelfProfileDetailView(SpecialistOnlyMixin, SpecialistProfileDetailView):
    def get_specialist(self):
        return self.request.user


def format_tel(tel: str) -> str:
    return tel


def format_inst(inst: str) -> str:
    return '@' + inst


def get_social_info(request):
    field_name = request.GET.get('field_name')
    is_mobile = True if request.GET.get('is_mobile') == 'true' else False
    specialist_username = request.GET.get('specialist')
    specialist = User.objects.get(username=specialist_username).specialist_profile

    try:
        contact_data = getattr(specialist, field_name)
        field_mapping = {
            'phone_number':
                {'info':
                     f"{contact_data[:2]} {contact_data[2:5]} {contact_data[5:8]}-{contact_data[8:10]}-{contact_data[10:12]}",
                 'href': f'tel:{contact_data}'},
            'telegram_profile': {'info': contact_data, 'href': f'https://t.me/{contact_data}'},
            'instagram_profile': {'info': f'@{contact_data}', 'href': f'https://www.instagram.com/{contact_data}'},
            'whatsapp': {'info': contact_data, 'href': f'https://wa.me/{contact_data}'},
        }
        info = field_mapping[field_name]['info']
        href = field_mapping[field_name]['href']
    except AttributeError:
        info = None
        href = None
    # Словарь для формирования ссылок в зависимости от типа соцсети

    # field_info = field_mapping.get(field_name, {'info_key': None, 'href_prefix': None})
    # info_key = field_info['info_key']
    # href_prefix = field_info['href_prefix']
    #
    # try:
    #     info = escape(getattr(specialist, info_key)) if info_key else None
    #     href = href_prefix + escape(getattr(specialist, field_name)) if href_prefix else None
    # except AttributeError:
    #     info = None
    #     href = None

    data = {'info': info, 'href': href}
    print(data)
    return JsonResponse(data)


class SpecialistPasswordChangeView(SpecialistOnlyMixin, MyPasswordChangeView):
    template_name = 'specialists/profile_change_password.html'


class SpecialistsListView(FilterFormMixin, ListView):
    model = SpecialistProfile
    paginate_by = 20
    template_name = 'specialists/specialists_list.html'
    context_object_name = 'specialists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мастер'
        context['filter_form'] = SpecialistFilterForm(self.request.GET)
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        return context

    def get_queryset(self):
        specialists = SpecialistProfile.objects.all()
        if self.request.user.is_authenticated and not self.request.user.is_specialist:
            specialists = add_is_bookmarked(queryset=specialists, user=self.request.user)
        form = SpecialistFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter(specialists)
        else:
            logging.error(form.errors)
        return queryset
