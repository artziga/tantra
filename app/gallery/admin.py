from django.contrib import admin
from gallery.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'admin_thumbnail',)


admin.site.register(Photo, PhotoAdmin)
