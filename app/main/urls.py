from django.urls import path
from main.views import index, ContactUsView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us')
]
