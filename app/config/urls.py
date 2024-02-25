from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('users/', include('users.urls')),
    path('specialists/', include('specialists.urls')),
    path('listings/', include('listings.urls')),
    path('gallery/', include('gallery.urls')),
    path('feedback/', include('feedback.urls')),
    path('articles/', include('articles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

