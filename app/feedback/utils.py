from feedback.models import Review


def get_reviews(obj):
    return Review.objects.filter(user=obj)
