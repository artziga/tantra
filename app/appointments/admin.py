from django.contrib import admin

from appointments.models import WorkSlots, Appointments


class WorkSlotsAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'day_of_week', 'start_time', 'end_time')


admin.site.register(WorkSlots, WorkSlotsAdmin)
admin.site.register(Appointments)
