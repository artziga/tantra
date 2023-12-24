from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render


class AddUserMixin:
    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs.pop('user')
        except KeyError:
            pass
        super().__init__(*args, **kwargs)


class SpecialistOnlyMixin(PermissionRequiredMixin):

    def has_permission(self):
        return self.request.user.is_authenticated and self.request.user.is_specialist

    def handle_no_permission(self):
        return render(self.request, 'accounts/403.html', status=403)



