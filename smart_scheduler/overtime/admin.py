from django.contrib import admin
from django.utils import timezone
from .models import OvertimeEntry

@admin.register(OvertimeEntry)
class OvertimeEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "shift_date", "hours", "note", "approved_on", "week_start_admin")
    list_filter = ("shift_date", "user", "approved_on")
    search_fields = ("user__username", "note")
    ordering = ("-shift_date",)
    autocomplete_fields = ("user",)
    date_hierarchy = "shift_date"

    @admin.display(description="Week start")
    def week_start_admin(self, obj):
        return obj.week_start

    @admin.action(description="Mark approved today")
    def mark_approved(self, request, queryset):
        queryset.update(approved_on=timezone.localdate())

    actions = ["mark_approved"]
    readonly_fields = ("approved_on",)   # ← prevents manual edits

