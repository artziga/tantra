import json
import logging

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from rest_framework.generics import ListAPIView

from feedback.forms import ReviewForm
from feedback.models import Review, Bookmark
from django.db.models import F, OuterRef, Value, BooleanField, Subquery

from feedback.serializers import ReviewSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


def add_is_bookmarked(queryset, user):
    """
        Добавляет атрибут is_bookmarked к queryset, указывающий,
        добавлен ли объект в избранное для конкретного пользователя.
    """

    if user and user.is_authenticated:
        bookmarked_subquery = Bookmark.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(User),
            object_id=OuterRef('pk')
        ).values('user').annotate(is_bookmarked=Value(True, output_field=BooleanField())).values('is_bookmarked')
        queryset = queryset.annotate(
            is_bookmarked=Subquery(bookmarked_subquery, output_field=BooleanField())
        )

    return queryset


class ReviewIntegrityError(Exception):
    pass


class AddReviewView(LoginRequiredMixin, View):
    """
    Класс для добавления отзыва.

    """

    def post(self, request):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    self.create_review()
            except ReviewIntegrityError as e:
                messages.error(request, str(e))
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))

    def create_review(self):
        score_value = self.request.POST.get('score')
        review_for = self.request.POST.get('review_for')
        text = self.request.POST.get('text')
        specialist = User.objects.get(pk=review_for)
        try:
            with transaction.atomic():
                Review.objects.create(author=self.request.user, text=text, score=score_value, user=specialist)
                logger.info(f"{self.request.user.username} оставил отзыв для {specialist}")
        except IntegrityError as e:
            logger.info(f"{e}!! {self.request.user.username} пытался оставить второй отзыв для {specialist}")
            raise ReviewIntegrityError("Only one review allowed per user.")


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления отзыва.

    """
    model = Review

    def get_success_url(self):
        return reverse_lazy('specialists:specialist_profile', args=[self.object.user.username])


class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user__username=self.kwargs['specialist_username'])


class BookmarkView(LoginRequiredMixin, View):
    """
    Класс для добавления или удаления избранного.

    """

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        obj_pk = data.get('obj_pk')
        content_type_id = data.get('content_type_id')
        user = auth.get_user(request)
        content_type = ContentType.objects.get_for_id(content_type_id)
        bookmark, created = Bookmark.objects.get_or_create(user=user, object_id=obj_pk, content_type=content_type)
        if not created:
            bookmark.delete()
        return HttpResponse(
            json.dumps({
                "result": created,
                "count": Bookmark.objects.filter(object_id=obj_pk).count()
            }),
            content_type="application/json"
        )
