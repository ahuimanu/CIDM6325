"""Airport models for TravelMathLite."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from django.db import models

from ..base.models import City, Country


class AirportQuerySet(models.QuerySet["Airport"]):
    """Typed queryset helpers for airports."""

    def active(self) -> AirportQuerySet:
        """Return active airports."""
        return self.filter(active=True)

    def search(self, term: str | None) -> AirportQuerySet:
        """Case-insensitive search across name, codes, and municipality."""
        if not term:
            return self.active()
        normalized = term.strip()
        return self.active().filter(
            models.Q(name__icontains=normalized)
            | models.Q(iata_code__icontains=normalized)
            | models.Q(ident__icontains=normalized)
            | models.Q(municipality__icontains=normalized)
            | models.Q(country__name__icontains=normalized)
        )

    def _bounding_box_filters(self, latitude: float, longitude: float, radius_km: float) -> dict[str, float]:
        """Return coordinate filters to pre-restrict the queryset."""
        radius_deg = radius_km / 111.0
        lat_min = latitude - radius_deg
        lat_max = latitude + radius_deg
        lon_delta = radius_deg / max(math.cos(math.radians(latitude)), 0.1)
        lon_min = longitude - lon_delta
        lon_max = longitude + lon_delta
        return {
            "latitude_deg__gte": lat_min,
            "latitude_deg__lte": lat_max,
            "longitude_deg__gte": lon_min,
            "longitude_deg__lte": lon_max,
        }

    def nearest(
        self,
        latitude: float,
        longitude: float,
        *,
        limit: int = 3,
        radius_km: float = 2000,
        iso_country: str | None = None,
        unit: Literal["km", "mi"] = "km",
    ) -> list[Airport]:
        """Return the closest airports ordered by haversine distance.

        Always attaches `distance_km` to returned Airport instances.
        When `unit="mi"`, also attaches `distance_mi`.
        """
        filters = self._bounding_box_filters(latitude, longitude, radius_km)
        qs = self.active().filter(**filters)
        if iso_country:
            qs = qs.filter(models.Q(country__iso_code__iexact=iso_country) | models.Q(iso_country__iexact=iso_country))

        candidates = list(qs)
        for airport in candidates:
            # Always compute and attach km distance
            d_km = _haversine_km(latitude, longitude, airport.latitude_deg, airport.longitude_deg)
            airport.distance_km = d_km
            if unit == "mi":
                from ..base.utils.units import km_to_mi

                airport.distance_mi = km_to_mi(d_km)
        candidates.sort(key=lambda airport: getattr(airport, "distance_km", math.inf))
        return candidates[:limit]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute haversine distance between two coordinates in kilometers."""
    radius = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


class Airport(models.Model):
    """
    Airport model based on OurAirports dataset.

    Fields map to OurAirports CSV columns for idempotent imports.
    """

    # Primary identifiers
    ident = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="ICAO or local airport code (primary key from OurAirports)",
    )
    iata_code = models.CharField(
        max_length=3,
        blank=True,
        db_index=True,
        help_text="IATA 3-letter code (preferred for display)",
    )

    # Core attributes
    name = models.CharField(max_length=255, help_text="Airport name")
    airport_type = models.CharField(
        max_length=50,
        help_text="Airport type (e.g., large_airport, medium_airport)",
    )

    # Location data
    latitude_deg = models.FloatField(help_text="Latitude in decimal degrees")
    longitude_deg = models.FloatField(help_text="Longitude in decimal degrees")
    elevation_ft = models.IntegerField(null=True, blank=True, help_text="Elevation in feet")

    # Geographic context
    iso_country = models.CharField(max_length=2, db_index=True, help_text="ISO 3166-1 country code")
    iso_region = models.CharField(max_length=10, blank=True, help_text="ISO 3166-2 region code")
    municipality = models.CharField(max_length=255, blank=True, help_text="City or town name")
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="airports",
        help_text="Normalized Country linked via iso_country",
    )
    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="airports",
        help_text="Normalized City derived from municipality",
    )
    active = models.BooleanField(default=True, help_text="Whether the airport is active/open")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Typing-only attributes attached at runtime by queryset helpers
    if TYPE_CHECKING:  # pragma: no cover - static typing aid only
        distance_km: float
        distance_mi: float

    objects: AirportQuerySet = AirportQuerySet.as_manager()  # type: ignore[assignment]

    class Meta:
        db_table = "airports"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["iata_code"]),
            models.Index(fields=["iso_country"]),
            models.Index(fields=["latitude_deg", "longitude_deg"]),
            models.Index(fields=["country"]),
            models.Index(fields=["city"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self) -> str:
        """Return string representation of airport."""
        if self.iata_code:
            return f"{self.name} ({self.iata_code})"
        return f"{self.name} ({self.ident})"
