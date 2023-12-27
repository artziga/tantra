from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'username', 'email', 'date_joined', 'is_active']
    list_display_links = ['pk', 'first_name', 'last_name', 'username']
    list_editable = ['is_active']

    def get_queryset(self, request):
        return User.objects.filter(is_specialist=False)


admin.site.register(User, UserAdmin)
