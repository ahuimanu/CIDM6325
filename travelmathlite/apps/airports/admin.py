"""Admin configuration for Airport model."""

from django.contrib import admin

from .models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """Expose normalized linkage information in the admin."""

    list_display = ("name", "iata_code", "ident", "country", "city", "active", "updated_at")
    list_filter = ("active", "airport_type", "country")
    search_fields = ("name", "iata_code", "ident", "municipality", "country__name", "city__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
