"""Admin registrations for normalized Country and City models."""

from django.contrib import admin

from .models import City, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin configuration for Country."""

    list_display = ("name", "iso_code", "iso3_code", "active", "latitude", "longitude")
    list_filter = ("active",)
    search_fields = ("name", "iso_code", "iso3_code")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin configuration for City."""

    list_display = ("name", "country", "timezone", "active")
    list_filter = ("active", "country")
    search_fields = ("name", "ascii_name", "country__name", "country__iso_code")
    ordering = ("country__name", "name")
    readonly_fields = ("created_at", "updated_at")
