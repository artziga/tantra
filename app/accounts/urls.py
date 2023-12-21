from django.contrib.auth import views
from django.urls import path, reverse_lazy

from accounts.forms import UserPasswordResetForm, LoginUserForm, MyPasswordChangeForm
from accounts.views import RegisterUserView, RegisterSpecialistView, RegistrationDone, user_activate, \
    MyPasswordResetConfirmView, MyLoginView

app_name = 'accounts'

urlpatterns = [
    path("registration/", RegisterUserView.as_view(), name="registration"),
    path("specialist_registration/", RegisterSpecialistView.as_view(), name="specialist_registration"),
    path("registration/done", RegistrationDone.as_view(), name="registration_done"),
    path("registration/activate/<str:sign>", user_activate, name="register_activate"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                        email_template_name="accounts/password_reset_email.html",
                                        success_url=reverse_lazy("accounts:password_reset_done"),
                                        form_class=UserPasswordResetForm),
        name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        MyPasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
