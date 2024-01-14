from django.views.generic import DetailView, ListView

from articles.models import Article, Announcement


class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    extra_context = {'title': 'Статья'}


class AnnouncementView(DetailView):
    model = Announcement
    context_object_name = 'announcement'
    extra_context = {'title': 'Анонс'}


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    extra_context = {'title': 'Статьи'}
    queryset = Article.objects.filter(published=True)


class AnnouncementListView(ListView):
    model = Announcement
    paginate_by = 10
    extra_context = {'title': 'Анонсы'}
    queryset = Announcement.objects.filter(published=True)
