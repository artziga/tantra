from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy

from articles.models import Article, Announcement
from main.forms import ContactUsForm

from django.views.generic import FormView, TemplateView

from config.settings import DEFAULT_FROM_EMAIL

User = get_user_model()


def index(request):
    return render(request, 'main/index.html')


class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {'title': 'tantra-massage.pro'}

    def get_context_data(self, **kwargs):
        articles = Article.objects.all()[:2]
        announcements = Announcement.objects.all()[:2]
        specialists = User.specialists.specialist_card_info().order_by('?')[:5]
        context = super().get_context_data(**kwargs)
        context['articles'] = articles
        context['announcements'] = announcements
        context['specialists'] = specialists
        return context


class ContactUsView(FormView):
    template_name = 'forms/simple_form.html'
    form_class = ContactUsForm
    extra_context = {
        'button_label': 'Отправить',
        'title': 'Обратная связь'
    }
    success_url = reverse_lazy('specialists:specialists')

    def form_valid(self, form):
        subject = 'Новое обращение'
        message = (f'Оращение от {form.cleaned_data.get("name", "неизвестного")}:'
                   f' \n{form.cleaned_data.get("text", "без текста")}'
                   f'\n{form.cleaned_data.get("name", "неизвестный")} '
                   f'ожидает ответ на электронную почту по адресу {form.cleaned_data.get("email", "???")}')
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = ['kazan-tantra@yandex.ru']

        send_mail(subject, message, from_email, recipient_list)  # TODO: Надо сделать асинхронно
        return super().form_valid(form)


class ProfileFillingRules(TemplateView):
    template_name = 'main/profile_filling_rules.html'
    extra_context = {'title': 'Правила размещения анкет'}
