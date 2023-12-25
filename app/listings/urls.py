from django.urls import path
from listings import views

app_name = 'listings'

urlpatterns = [
    path('create_offer/<str:username>/', views.OfferCreateView.as_view(), name='create_offer'),
    path('update_offer/<int:pk>/', views.OfferUpdateView.as_view(), name='update_offer'),
    path('remove_offer/<int:pk>/', views.remove_offer, name='remove_offer'),
]
