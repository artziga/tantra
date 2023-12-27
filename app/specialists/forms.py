from django import forms
from django.db.models import Q

from listings.models import MassageFor, Feature, BasicService, BasicServicePrice
from specialists.mixins import AddUserMixin
from config.utils import Locator
from specialists.models import validate_age, SpecialistProfile


class PersonDataForm(AddUserMixin, forms.Form):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Фамилия'}))
    gender = forms.NullBooleanField(label='Пол', widget=forms.Select(attrs={'class': 'form__input'},
                                                                     choices=(
                                                                         (None, 'Укажите свой пол'), (True, 'Мужчина'),
                                                                         (False, 'Женщина'))))
    birth_date = forms.DateField(label='Дата рождения', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
                                 validators=[validate_age])
    height = forms.IntegerField(required=False, label='Рост', widget=forms.NumberInput(attrs={'class': 'form__input'}))
    weight = forms.IntegerField(required=False, label='Вес', widget=forms.NumberInput(attrs={'class': 'form__input'}))

    @staticmethod
    def get_initial(user):
        profile_data = SpecialistProfile.objects.select_related('user').filter(user=user).values(
            'user__first_name',
            'user__last_name',
            'gender',
            'birth_date',
            'height',
            'weight'
        ).first()
        if profile_data:
            initial = {
                'first_name': profile_data['user__first_name'],
                'last_name': profile_data['user__last_name'],
                'gender': profile_data['gender'],
                'height': profile_data['height'],
                'weight': profile_data['weight'],
            }
            bd = profile_data['birth_date']
            if bd:
                initial['birth_date'] = bd.isoformat()
        else:
            initial = {}
        return initial


class SpecialistDataForm(AddUserMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['massage_for'].choices = MassageFor.objects.values_list('pk', 'massage_for')

    massage_for = forms.MultipleChoiceField(label='Для кого вы делаете массаж',
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple(),
                                            )
    practice_start_date = forms.DateField(label='Дата начала практики', required=False,
                                          widget=forms.DateInput(
                                              attrs={'type': 'date', 'class': 'form__input'}))

    home_price = forms.IntegerField(label='Цена базовой программы дома, ₽',
                                    widget=forms.NumberInput(attrs={'class': 'form__input'}))
    on_site_price = forms.IntegerField(label='Цена базовой программы с выездом, ₽',
                                       widget=forms.NumberInput(attrs={'class': 'form__input'}))

    @staticmethod
    def get_initial(user):
        initial = {}
        profile_data = SpecialistProfile.objects.filter(user=user).values(
            'practice_start_date',
            'massage_for',
        ).first()
        mf = SpecialistProfile.objects.filter(user=user).values_list('massage_for', flat=True).all()
        if mf:
            initial['massage_for'] = list(mf)
        if profile_data:
            psd = profile_data.get('practice_start_date')
            if psd:
                initial['practice_start_date'] = psd.isoformat()
        bs = BasicService.objects.get(pk=1)
        prices = BasicServicePrice.objects.filter(
            service=bs,
            specialist=SpecialistProfile.objects.get(user=user)
        ).values('home_price', 'on_site_price').first()
        if prices:
            initial.update(prices)
        return initial


class AboutForm(AddUserMixin, forms.Form):
    description = forms.CharField(required=False, label='О себе', widget=forms.Textarea(
        attrs={'class': 'form__input form__input--about--textarea'}))

    @staticmethod
    def get_initial(user):
        initial = {}
        description = SpecialistProfile.objects.filter(user=user).values(
            'description',
        ).first()
        formatted_description = description['description']
        initial['description'] = formatted_description
        return initial


class ContactDataForm(AddUserMixin, forms.Form):
    address = forms.CharField(required=False, label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Введите адрес', 'id': 'addressInput'}))
    phone_number = forms.CharField(required=False, label='Телефон', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Введите телефон'}))
    telegram_profile = forms.CharField(required=False, label='Телеграм', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Введите ваш ник'}))
    instagram_profile = forms.CharField(required=False, label='Инстаграм', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Введите ваш ник'}))

    @staticmethod
    def get_initial(user):
        initial = SpecialistProfile.objects.filter(user=user).values(
            'address',
            'phone_number',
            'telegram_profile',
            'instagram_profile',
        ).first()
        return initial

    def clean(self):
        cleaned_data = self.cleaned_data
        current_address = None
        if self.user.is_specialist:
            current_address = self.user.specialist_profile.address
        new_address = cleaned_data['address']
        if new_address:
            if current_address and new_address == current_address:
                return
            else:
                raw_address = cleaned_data['address']
                place = Locator(raw_place=raw_address).location()
                self.cleaned_data['address'] = place
                self.cleaned_data['latitude'] = place.point.latitude
                self.cleaned_data['longitude'] = place.point.longitude
        print(cleaned_data)
        return self.cleaned_data

    # def clean_address_data(self, user):
    #     cleaned_data = self.cleaned_data
    #     current_address = None
    #     if user.is_specialist:
    #         current_address = user.specialist_profile.address
    #     new_address = cleaned_data['address']
    #     print(new_address)
    #     print(current_address)
    #     if new_address:
    #         if current_address and new_address == current_address:
    #             return
    #         else:
    #             raw_address = cleaned_data['address']
    #             place = Locator(raw_place=raw_address).location()
    #             self.cleaned_data['address'] = place
    #             self.cleaned_data['latitude'] = place.point.latitude
    #             self.cleaned_data['longitude'] = place.point.longitude
    #     print(cleaned_data)
    #     return self.cleaned_data


class ActivateProfileForm(AddUserMixin, forms.Form):
    is_profile_active = forms.BooleanField(required=False)


price_range = {'low': (1000, 3000), 'medium': (3000, 7000), 'high': (7000, 20000)}
ORDERINGS = (('-rating__average', 'Рейтинг'),
             ('min_price', '<i class="fa fa-arrow-up" aria-hidden="true">Цена</i>'),
             ('-min_price', '<i class="fa fa-arrow-down" aria-hidden="true">Цена</i>'),
             ('-specialist_profile__birth_date', '<i class="fa fa-arrow-up" aria-hidden="true">Возраст</i>'),
             ('specialist_profile__birth_date', '<i class="fa fa-arrow-down" aria-hidden="true">Возраст</i>'),
             ('specialist_profile__practice_start_date', 'Опыт'),
             ('-rating__count', 'Количество отзывов'),
             ('-date_joined', 'Сначала новые'))


class SpecialistFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['massage_for'].choices = MassageFor.objects.values_list('slug', 'massage_for')

    gender = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(True, 'Мужчина'), (False, 'Женщина')],
    )

    massage_for = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    price = forms.ChoiceField(required=False,
                              widget=forms.RadioSelect,
                              choices=[(key, f'₽{price_range[key][0]} - ₽{price_range[key][1]}') for key in price_range]
                              )

    order_by = forms.ChoiceField(
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )

    def get_query_params(self):
        query_params = {}
        for key, value in self.cleaned_data.items():
            if value:
                query_params[key] = value
        return query_params

    def filter(self, queryset):
        genders = self.cleaned_data.get('gender') or [True, False]
        massage_for = self.cleaned_data.get('massage_for') or ['for_males', 'for_females', 'for_pairs']
        price = self.cleaned_data.get('price')
        queryset = (queryset.
                    filter(
            specialist_profile__gender__in=genders,
            specialist_profile__massage_for__slug__in=massage_for
        )
                    .distinct())
        if price:
            price_filter = Q(min_price__gte=price_range[price][0], min_price__lte=price_range[price][1])
            queryset = queryset.filter(price_filter)
        ordering = self.cleaned_data.get('order_by')

        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class FeaturesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        features = Feature.objects.values_list('id', 'name')
        for massage_for_id, massage_for_name in features:
            field_name = f'feature_{massage_for_id}'
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=massage_for_name,
                widget=forms.CheckboxInput()
            )


class OrderingForm(forms.Form):
    order_by = forms.ChoiceField(
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )
