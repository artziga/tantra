from django.urls import path

from articles.views import ArticleView, ArticleListView, AnnouncementListView, AnnouncementView

app_name = 'articles'

urlpatterns = [
    path("", ArticleListView.as_view(), name="articles_list"),
    path("announcement/", AnnouncementListView.as_view(), name="announcements_list"),
    path("announcement/<str:slug>", AnnouncementView.as_view(), name="announcement_detail"),
    path("article/<str:slug>", ArticleView.as_view(), name="article_detail"),
]
