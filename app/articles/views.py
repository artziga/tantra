from django.views.generic import DetailView, ListView

from articles.models import Article, Announcement
from articles.utils import get_upcoming_events


class ArticleView(DetailView):
    """
    Класс представления для отображения деталей статьи.

    """

    model = Article
    context_object_name = 'article'
    extra_context = {'title': 'Статья'}


class AnnouncementView(DetailView):
    """
    Класс представления для отображения деталей анонса.

    """

    model = Announcement
    context_object_name = 'announcement'
    extra_context = {'title': 'Анонс'}


class ArticleListView(ListView):
    """
    Класс представления для отображения списка статей.

    """

    model = Article
    paginate_by = 10
    extra_context = {'title': 'Статьи'}
    queryset = Article.objects.filter(published=True)


class AnnouncementListView(ListView):
    """
    Класс представления для отображения списка анонсов.

    """

    model = Announcement
    paginate_by = 10
    extra_context = {'title': 'Анонсы'}
    queryset = get_upcoming_events()
