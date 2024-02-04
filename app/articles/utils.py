from datetime import date

from articles.models import Announcement


def get_upcoming_events():
    today = date.today()
    upcoming_events = Announcement.objects.filter(published=True, event_time__gt=today)
    return upcoming_events