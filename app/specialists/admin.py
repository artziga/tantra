from django.contrib import admin
from users.models import User
from specialists.models import SpecialistProfile


class SpecialistAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'get_first_name',
        'get_last_name',
        'get_username',
        'get_email',
        'get_date_joined',
        'get_is_active',
        'gender',
        'is_profile_active'
    ]
    list_display_links = ['pk', 'get_first_name', 'get_last_name', 'get_username', ]
    list_editable = ['is_profile_active']

    # list_editable = ['email', 'is_active']

    def get_queryset(self, request):
        return SpecialistProfile.objects.select_related('user').filter(user__is_specialist=True).order_by(
            'is_profile_active')

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Фамилия'

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'username'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'email'

    def get_date_joined(self, obj):
        return obj.user.date_joined

    get_date_joined.short_description = 'Дата регистрации'

    def get_is_active(self, obj):
        return obj.user.is_active

    get_is_active.short_description = 'Активен'


admin.site.register(SpecialistProfile, SpecialistAdmin)
