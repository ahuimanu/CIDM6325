from django.contrib import admin
from .models import Shift, Availability

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display  = ("starts_at", "ends_at", "status", "assigned_to", "role", "location")
    list_filter   = ("status", "role", "location")
    search_fields = ("assigned_to__username", "role", "location")
    date_hierarchy = "starts_at"

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display  = ("user", "date", "is_available")
    list_filter   = ("is_available",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    date_hierarchy = "date"


# Register your models here.
