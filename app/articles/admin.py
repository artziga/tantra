from django.contrib import admin

from articles.models import Article, Announcement

admin.site.register(Article)
admin.site.register(Announcement)

