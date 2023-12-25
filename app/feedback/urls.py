from django.urls import path
from feedback.views import AddReviewView, delete_review, BookmarkView

app_name = 'feedback'

urlpatterns = [
    path('like/', BookmarkView.as_view(), name='like'),
    path('add/', AddReviewView.as_view(), name='add_comment'),
    path('delete/<int:review_for>/', delete_review, name='delete_review'),
    path('<str:from_user>/<int:parent_comment_id>/', AddReviewView.as_view(), name='add_comment_with_parent'),
]

