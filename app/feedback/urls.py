from django.urls import path
from feedback.views import AddReviewView, BookmarkView, DeleteReviewView, ReviewListView

app_name = 'feedback'

urlpatterns = [
    path('like/', BookmarkView.as_view(), name='like'),
    path('add/', AddReviewView.as_view(), name='add_comment'),
    path('delete/<int:pk>/', DeleteReviewView.as_view(), name='delete_review'),
    path('<str:from_user>/<int:parent_comment_id>/', AddReviewView.as_view(), name='add_comment_with_parent'),
    path('api/v1/specialists/<str:specialist_username>/comments', ReviewListView.as_view()),
]

