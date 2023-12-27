from django.urls import path


from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('avatar/', views.AddAvatar.as_view(), name='add_avatar'),
    path('favorite/', views.Favorite.as_view(), name='favorite'),
    path('edit_profile/<str:username>', views.EditProfile.as_view(), name='edit_profile'),
    path(
        "password_change/", views.UserPasswordChangeView.as_view(), name="change_password"
    ),
]





