from django.urls import path
from main.views import index, ContactUsView, IndexView

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us')
]
