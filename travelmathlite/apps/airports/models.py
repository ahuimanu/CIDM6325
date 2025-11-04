"""Airport models for TravelMathLite."""

from django.db import models


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

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "airports"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["iata_code"]),
            models.Index(fields=["iso_country"]),
            models.Index(fields=["latitude_deg", "longitude_deg"]),
        ]

    def __str__(self) -> str:
        """Return string representation of airport."""
        if self.iata_code:
            return f"{self.name} ({self.iata_code})"
        return f"{self.name} ({self.ident})"
