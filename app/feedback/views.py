import json
import logging

from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, F, Subquery, BooleanField, Value, OuterRef, Exists
from django.db.utils import IntegrityError
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from rest_framework import viewsets, mixins, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from feedback.forms import ReviewForm
from feedback.models import Review, Bookmark

from feedback.serializers import ReviewSerializer
from feedback.templatetags.rating_tags import rating_class

User = get_user_model()

logger = logging.getLogger(__name__)


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


class ReviewPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        avg_rating = queryset.aggregate(avg=Avg('score'))['avg']
        avg_rating_class = rating_class(avg_rating)
        page = self.paginate_queryset(queryset)
        rating_metadata = {
            'average_rating_class': avg_rating_class,
        }
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            paginated_response.data.update(rating_metadata)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        data = rating_metadata.update(serializer.data)
        return Response(data)

    def get_queryset(self):
        queryset = Review.objects.filter(user__username=self.kwargs['specialist_username'])

        return queryset

    def perform_create(self, serializer):
        specialist = self.kwargs['specialist_username']
        specialist = get_object_or_404(User, username=specialist)
        serializer.save(author=self.request.user, user=specialist)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        specialist_username = self.kwargs['specialist_username']
        if Review.objects.filter(author=self.request.user, user__username=specialist_username).exists():
            return Response({"error": "Отзыв уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RatingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_reviews_exists = Exists(
            Review.objects.filter(author=self.request.user, user=OuterRef('pk')))
        specialist = (User.objects.filter(username=self.kwargs['specialist_username'])
                      .annotate(average_rating=Avg('review_for__score'), is_reviewed=user_reviews_exists)
                      .values('average_rating', 'is_reviewed').get())
        return Response(specialist, status=status.HTTP_200_OK)


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
