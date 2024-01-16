import logging
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db.models import F, OuterRef, Value, BooleanField, Subquery, Prefetch, Count, Avg
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.conf import settings
from formtools.wizard.views import SessionWizardView

from accounts.views import MyPasswordChangeView
from feedback.forms import ReviewForm
from feedback.models import Bookmark, Review
from feedback.utils import get_reviews
from feedback.views import add_is_bookmarked
from gallery.models import Photo
from listings.models import Listing
from specialists.models import BasicService, BasicServicePrice
from specialists.forms import PersonDataForm, SpecialistDataForm, ContactDataForm, AboutForm, SpecialistFilterForm, \
    FeaturesForm
from specialists.mixins import SpecialistOnlyMixin, specialist_only
from specialists.utils import make_user_a_specialist, delete_specialist, filter_specialists
from main.utils import FilterFormMixin
from specialists.models import SpecialistProfile
from users.views import ProfileView

User = get_user_model()

FORMS = [
    ("person_data", PersonDataForm),
    ("specialist_data", SpecialistDataForm),
    ("contact_data", ContactDataForm),
    ("features", FeaturesForm),
    ("about", AboutForm),
]


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
        return 'forms/wizard_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Анкета'
        context['not_delete'] = True
        context['YANDEX_API_KEY'] = settings.YANDEX_GEOCODER_API_KEY
        context['GEOSUGGEST_KEY'] = settings.YANDEX_GEOSUGGEST_API_KEY
        return context

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        user = self.request.user
        user.first_name = cleaned_data.pop('first_name', '')
        user.last_name = cleaned_data.pop('last_name', '')
        massage_for_set = cleaned_data.pop('massage_for', [])
        features_set = cleaned_data.pop('features', [])
        home_price = cleaned_data.pop('home_price', '')
        on_site_price = cleaned_data.pop('on_site_price', '')
        if not user.is_specialist:
            goto = redirect('gallery:edit_gallery')
            make_user_a_specialist(user)
        else:
            goto = redirect('specialists:profile')
        tp, created = SpecialistProfile.objects.update_or_create(user=user, defaults=cleaned_data)
        self.set_price(data={
            'home_price': home_price,
            'on_site_price': on_site_price
        },
            tp=tp
        )
        tp.massage_for.set(massage_for_set)
        tp.features.set(features_set)
        user.save()
        tp.save()
        logging.info(f"Заполнена анкета пользователем {user}")
        return goto

    def set_price(self, data, tp):
        bs = BasicService.objects.get(pk=1)
        defaults = data
        query_params = {'specialist': tp, 'service': bs}
        create_defaults = defaults.copy()
        create_defaults.update(query_params)
        BasicServicePrice.objects.update_or_create(
            **query_params,
            defaults=defaults,
            create_defaults=create_defaults
        )

    def get_form_initial(self, step):
        forms = dict(FORMS)
        form = forms[step]
        initial = form.get_initial(self.request.user)

        return initial


class SpecialistProfileDetailView(ProfileView):
    template_name = 'specialists/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        specialist = self.get_specialist()
        offers = Listing.objects.filter(specialist_id=specialist.pk)
        photos = Photo.objects.filter(user=specialist)
        ct = ContentType.objects.get_for_model(specialist)
        reviews = get_reviews(specialist)
        is_reviewed = self.request.user in [review.author for review in reviews]
        review_form = self.get_review_form(specialist=specialist)
        context['is_reviewed'] = is_reviewed
        context['specialist'] = specialist
        context['content_type_id'] = ct.pk
        context['offers'] = offers
        context['all_photos'] = photos
        context['count'] = Bookmark.objects.filter(object_id=specialist.pk, content_type_id=ct.pk).count()
        context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=ct.pk,
                                                           user_id=self.request.user.pk,
                                                           object_id=specialist.pk).exists()
        context['reviews'] = reviews
        context['form'] = review_form
        context['listings'] = specialist.listings.all()
        return context

    def get_specialist(self):
        specialist_name = self.kwargs.get('specialist_username', self.request.user.username)
        print(specialist_name)
        # specialist = get_object_or_404(User, username=specialist_name)

        specialist = User.objects.filter(username=specialist_name)
        review = Prefetch('review_for', queryset=Review.objects.all(), to_attr='score')
        sp = (specialist.select_related('specialist_profile').prefetch_related(review))

        sp = sp.annotate(
            min_price=F('specialist_profile__basicserviceprice__home_price'),
            # TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
            num_reviews=Count('review_for', distinct=True),
            avg_score=Avg('review_for__score'))
        specialist = sp.first()
        print(specialist.avg_score)
        return specialist

    @staticmethod
    def get_review_form(specialist):
        review_form = ReviewForm()
        review_form.fields['review_for'].initial = specialist.pk
        return review_form


class SpecialistSelfProfileDetailView(SpecialistOnlyMixin, SpecialistProfileDetailView):
    pass
    # def get_specialist(self):
    #     return self.request.user


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

    data = {'info': info, 'href': href}
    print(data)
    return JsonResponse(data)


class SpecialistPasswordChangeView(SpecialistOnlyMixin, MyPasswordChangeView):
    template_name = 'specialists/profile_change_password.html'


class SpecialistsListView(FilterFormMixin, ListView):
    model = User
    paginate_by = 10
    template_name = 'specialists/specialists_list.html'
    context_object_name = 'specialists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мастер'
        context['filter_form'] = SpecialistFilterForm(self.request.GET)
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        context['YANDEX_API_KEY'] = settings.YANDEX_GEOCODER_API_KEY
        return context

    def get_queryset(self):
        specialists = User.specialists.specialist_card_info()
        if self.request.user.is_authenticated and not self.request.user.is_specialist:
            specialists = add_is_bookmarked(queryset=specialists, user=self.request.user)
        form = SpecialistFilterForm(self.request.GET)
        if form.is_valid():
            filter_parameters = self.request.GET
            queryset = filter_specialists(specialists, filter_parameters)
        else:
            logging.error(form.errors)
        return queryset


def specialists_on_map_list(request):
    get_parameters = request.GET
    filter_params = get_parameters
    specialists = User.specialists.active()
    if filter_params:
        specialists = filter_specialists(specialists, filter_params, for_map=True)
    specialists_data = []
    lat = 0
    long = 0
    count = 0
    for specialist in specialists:
        specialists_data.append(
            {
                'username': specialist.username,
                'avatar': specialist.avatar.image.url,
                'name': specialist.get_full_name(),
                'point': specialist.specialist_profile.point,
                'url': reverse('specialists:specialist_profile', kwargs={'specialist_username': specialist.username})
            }
        )
        lat += specialist.specialist_profile.latitude
        long += specialist.specialist_profile.longitude
        count += 1
    map_center = (lat/count, long/count)
    return JsonResponse({'specialists_for_map': specialists_data, 'map_center': map_center})
