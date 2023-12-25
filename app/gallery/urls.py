from django.urls import path
from gallery import views
from gallery.views import change_avatar, change_avatar_confirm

app_name = 'gallery'

urlpatterns = [
    path('edit_gallery/', views.EditGallery.as_view(), name='edit_gallery'),
    path('delete_photo/<int:pk>', views.PhotoDeleteView.as_view(), name='delete_photo'),
    path('change_avatar/<int:pk>', change_avatar, name='change_avatar'),
    path('change_avatar_confirmation/<int:pk>', change_avatar_confirm, name='change_avatar_confirmation'),
]
