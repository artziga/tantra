from django.contrib import admin
from gallery.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'thumbnail',)


admin.site.register(Photo, PhotoAdmin)
