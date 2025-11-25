from django.contrib import admin

from .models import SavedCalculation


@admin.register(SavedCalculation)
class SavedCalculationAdmin(admin.ModelAdmin):
    """Admin interface for SavedCalculation model."""

    list_display = ["user", "calculator_type", "created_at", "id"]
    list_filter = ["calculator_type", "created_at"]
    search_fields = ["user__username", "calculator_type"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def get_queryset(self, request):
        """Optimize queryset with select_related for user FK."""
        qs = super().get_queryset(request)
        return qs.select_related("user")
