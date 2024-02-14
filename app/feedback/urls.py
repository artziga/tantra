from django.urls import path

from feedback.views import AddReviewView, BookmarkView, DeleteReviewView, ReviewViewSet, RatingAPIView

app_name = 'feedback'

urlpatterns = [
    path('like/', BookmarkView.as_view(), name='like'),
    path('add/', AddReviewView.as_view(), name='add_comment'),
    path('delete/<int:pk>/', DeleteReviewView.as_view(), name='delete_review'),
    path('<str:from_user>/<int:parent_comment_id>/', AddReviewView.as_view(), name='add_comment_with_parent'),
    path('api/v1/specialists/<str:specialist_username>/reviews/',
         ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='reviews_api'),
    path('api/v1/specialists/<str:specialist_username>/reviews/<int:pk>', ReviewViewSet.as_view({'delete': 'destroy'}),
         name='delete_reviews_api'),
    path('api/v1/specialists/<str:specialist_username>/rating', RatingAPIView.as_view(),
         name='delete_reviews_api'),
]
