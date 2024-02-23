from django.urls import path

from appointments.views import SlotsViewSet

app_name = 'appointments'

urlpatterns = [
    path('api/v1/specialists/<str:specialist_username>/slots/',
         SlotsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/specialists/<str:specialist_username>/reviews/<int:pk>/',
         SlotsViewSet.as_view({'delete': 'destroy', 'put': 'update'})),
]
