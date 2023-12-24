from django.urls import path


from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('avatar/', views.AddAvatar.as_view(), name='add_avatar'),
    # path('favorite/', views.Favorite.as_view(), name='favorite'),
    path('edit_profile/<str:username>', views.EditProfile.as_view(), name='edit_profile'),
    path(
        "password_change/", views.UserPasswordChangeView.as_view(), name="change_password"
    ),
    path('', views.SpecialistsListView.as_view(), name='specialists'),

    path('profile/', views.SpecialistSelfProfileDetailView.as_view(), name='profile'),
    path('become_a_specialist/', views.become_a_specialist, name='become_a_specialist'),
    path('delete_a_specialist/', views.delete_specialist_profile, name='delete_a_specialist'),
    path('delete_a_specialist/confirm/', views.delete_a_specialist_confirmation,
         name='delete_a_specialist_confirmation'),
    path('edit_profile/<str:username>', views.SpecialistProfileWizard.as_view(), name='edit_profile'),
    path(
        "password_change/", views.SpecialistPasswordChangeView.as_view(), name="change_password"
    ),
    path('get_social_info/', views.get_social_info, name='get_social_info'),
    path('<str:specialist_username>/', views.SpecialistProfileDetailView.as_view(), name='specialist_profile'),
]





