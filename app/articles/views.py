from django.shortcuts import render
from django.views.generic import TemplateView


class ArticleView(TemplateView):
    template_name = 'articles/article.html'
    context_object_name = 'article'
    extra_context = {'title': 'Статья'}

