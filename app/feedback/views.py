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
from star_ratings.models import Rating, UserRating
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from feedback.forms import ReviewForm
from feedback.models import Review, Bookmark
from django.db.models import F, OuterRef, Value, BooleanField, Subquery

User = get_user_model()

logger = logging.getLogger(__name__)


def add_is_bookmarked(queryset, user):
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


@login_required
def delete_review(request, review_for):
    review_from = request.user
    try:
        specialist = User.objects.get(pk=review_for)
        ct = ContentType.objects.get_for_model(specialist)
        rating = Rating.objects.get(object_id=specialist.pk, content_type=ct)
        user_rating = UserRating.objects.get(user=review_from, rating=rating)
        user_rating.delete()
        logger.info(f"{request.user.username} удалил отзыв для {specialist}")
    except UserRating.DoesNotExist as e:
        logger.error(f"Ошибка удаления отзыва {request.user.username}: {e}")

    return redirect(request.META.get('HTTP_REFERER'))


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review

    def get_success_url(self):
        return reverse_lazy('specialists:specialist_profile', args=[self.object.user.username])


class BookmarkView(LoginRequiredMixin, View):

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
