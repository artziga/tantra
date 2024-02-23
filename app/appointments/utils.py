from appointments.models import WorkSlots


def get_specialists_work_slots(username):
    return WorkSlots.objects.filter(specialist__user__username=username)