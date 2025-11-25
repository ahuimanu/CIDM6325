"""Core normalized Country and City models used across the project."""

from __future__ import annotations

from typing import Any

from django.db import models
from django.utils.text import slugify


class TimestampedModel(models.Model):
    """Abstract base for created/updated tracking."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryQuerySet(models.QuerySet["Country"]):
    """Custom queryset helpers for Country."""

    def active(self) -> CountryQuerySet:
        """Return only active countries."""
        return self.filter(active=True)

    def search(self, term: str | None) -> CountryQuerySet:
        """Search countries by name or ISO code."""
        if not term:
            return self.active()
        normalized = term.strip().lower()
        return self.active().filter(models.Q(search_name__icontains=normalized) | models.Q(iso_code__icontains=normalized))


class Country(TimestampedModel):
    """Normalized country model keyed by ISO alpha-2 code."""

    iso_code = models.CharField(
        max_length=2,
        unique=True,
        help_text="ISO 3166-1 alpha-2 code (e.g., US, CA, MX)",
    )
    name = models.CharField(max_length=128, help_text="Display name for the country")
    iso3_code = models.CharField(max_length=3, blank=True, help_text="Optional ISO alpha-3 code")
    numeric_code = models.CharField(max_length=3, blank=True, help_text="Optional numeric ISO code")
    search_name = models.CharField(max_length=128, db_index=True, help_text="Lowercase friendly name used for searches")
    slug = models.SlugField(max_length=64, unique=True, help_text="URL-friendly identifier")
    latitude = models.FloatField(null=True, blank=True, help_text="Representative latitude (optional centroid)")
    longitude = models.FloatField(null=True, blank=True, help_text="Representative longitude (optional centroid)")
    active = models.BooleanField(default=True, help_text="Whether the country is available for lookups")

    objects = CountryQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Normalize fields before saving."""
        if self.iso_code:
            self.iso_code = self.iso_code.upper()
        self.name = self.name.strip()
        self.search_name = self.name.lower()
        if not self.slug:
            self.slug = slugify(f"{self.iso_code}-{self.name}") or self.iso_code.lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"{self.name} ({self.iso_code})"


class CityQuerySet(models.QuerySet["City"]):
    """Query helpers for City."""

    def active(self) -> CityQuerySet:
        """Return active cities only."""
        return self.filter(active=True)

    def search(self, term: str | None) -> CityQuerySet:
        """Search cities by case-insensitive name."""
        if not term:
            return self.active()
        normalized = term.strip().lower()
        return self.active().filter(search_name__icontains=normalized)


class City(TimestampedModel):
    """Normalized city model linked to Country."""

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="cities",
        help_text="Country the city belongs to",
    )
    name = models.CharField(max_length=255, help_text="Canonical city name")
    ascii_name = models.CharField(max_length=255, blank=True, help_text="ASCII-safe variant of the name")
    search_name = models.CharField(max_length=255, db_index=True, help_text="Lowercase normalized name used for search")
    slug = models.SlugField(max_length=255, help_text="URL-friendly identifier unique per country")
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude (optional centroid)")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude (optional centroid)")
    timezone = models.CharField(max_length=64, blank=True, help_text="Timezone identifier if available")
    population = models.IntegerField(null=True, blank=True, help_text="Optional population estimate")
    active = models.BooleanField(default=True, help_text="Whether the city is available for lookups")

    objects = CityQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["country", "search_name"],
                name="city_country_search_unique",
            ),
            models.UniqueConstraint(
                fields=["country", "slug"],
                name="city_country_slug_unique",
            ),
        ]
        indexes = [
            models.Index(fields=["country", "search_name"]),
            models.Index(fields=["country", "slug"]),
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Normalize name, search, and slug before saving."""
        self.name = self.name.strip()
        if not self.ascii_name:
            self.ascii_name = self.name
        normalized = self.ascii_name.lower()
        self.search_name = normalized
        if not self.slug:
            base = f"{self.country.iso_code}-{self.ascii_name}"
            self.slug = slugify(base)[:255] or slugify(self.ascii_name)[:255]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"{self.name}, {self.country.iso_code}"
