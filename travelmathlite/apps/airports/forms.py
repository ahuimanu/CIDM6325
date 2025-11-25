"""Forms for airport-related user inputs and validation.

Implements `NearestAirportForm` per ADR-1.0.3 brief to accept a flexible
query (city, IATA, or coordinates) and normalize it to coordinates.
"""

from __future__ import annotations

import re
from typing import Literal

from django import forms

from ..base.models import City
from .models import Airport

LAT_LON_RE = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*$")


class NearestAirportForm(forms.Form):
    """Form that resolves a user-supplied location to coordinates.

    Supports three input modes via the `query` field:
    - City name (matches normalized `City` or airport `municipality`)
    - IATA code (3 letters)
    - Raw coordinates in the form "lat,lon"

    On successful validation, sets `resolved_coords` to a tuple of
    ``(latitude, longitude)`` in decimal degrees.
    """

    query = forms.CharField(max_length=255, required=True)
    iso_country = forms.CharField(max_length=2, required=False)
    unit = forms.ChoiceField(choices=(("km", "km"), ("mi", "mi")), initial="km", required=False)
    limit = forms.IntegerField(min_value=1, max_value=10, initial=3, required=False)

    resolved_coords: tuple[float, float] | None = None

    def clean_iso_country(self) -> str:
        """Normalize ISO country code to uppercase when provided."""
        code = (self.cleaned_data.get("iso_country") or "").strip()
        if not code:
            return ""
        if len(code) != 2:
            raise forms.ValidationError("ISO country code must be 2 letters (e.g., 'US').")
        return code.upper()

    def clean_unit(self) -> Literal["km", "mi"]:
        unit = (self.cleaned_data.get("unit") or "km").strip().lower()
        if unit not in {"km", "mi"}:
            raise forms.ValidationError("Unit must be 'km' or 'mi'.")
        return unit  # type: ignore[return-value]

    def clean_limit(self) -> int:
        value = self.cleaned_data.get("limit")
        if value in (None, ""):
            return 3
        try:
            ivalue = int(value)
        except (TypeError, ValueError) as err:
            raise forms.ValidationError("Limit must be an integer.") from err
        if ivalue < 1:
            raise forms.ValidationError("Limit must be at least 1.")
        if ivalue > 10:
            raise forms.ValidationError("Limit must be at most 10.")
        return ivalue

    def clean_query(self) -> str:
        value = (self.cleaned_data.get("query") or "").strip()
        if not value:
            raise forms.ValidationError("Please enter a city, IATA code, or coordinates (lat,lon).")
        return value

    def clean(self) -> dict:
        cleaned = super().clean()
        if self.errors:
            return cleaned

        query = cleaned.get("query") or ""
        iso_country = cleaned.get("iso_country") or ""

        # 1) Direct coordinates: "lat,lon"
        coords = self._try_parse_coords(query)
        if coords:
            self.resolved_coords = coords
            return cleaned

        # 2) IATA code (3 letters)
        if self._looks_like_iata(query):
            coords = self._resolve_iata(query, iso_country)
            if coords:
                self.resolved_coords = coords
                return cleaned
            self.add_error("query", "Unknown or unsupported IATA code.")
            return cleaned

        # 3) City name lookup (normalized City first, then Airport.municipality)
        coords = self._resolve_city_or_municipality(query, iso_country)
        if coords:
            self.resolved_coords = coords
            return cleaned

        self.add_error("query", "Could not resolve to a location. Try a city, IATA code, or lat,lon.")
        return cleaned

    # Helpers
    def _try_parse_coords(self, value: str) -> tuple[float, float] | None:
        match = LAT_LON_RE.match(value)
        if not match:
            return None
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
        except ValueError:
            return None
        if not (-90.0 <= lat <= 90.0):
            self.add_error("query", "Latitude must be between -90 and 90.")
            return None
        if not (-180.0 <= lon <= 180.0):
            self.add_error("query", "Longitude must be between -180 and 180.")
            return None
        return lat, lon

    def _looks_like_iata(self, value: str) -> bool:
        return len(value) == 3 and value.replace(" ", "").isalpha()

    def _resolve_iata(self, code: str, iso_country: str) -> tuple[float, float] | None:
        qs = Airport.objects.active().filter(iata_code__iexact=code)
        if iso_country:
            qs = qs.filter(iso_country__iexact=iso_country)
        airport = qs.first()
        if not airport:
            return None
        return float(airport.latitude_deg), float(airport.longitude_deg)

    def _resolve_city_or_municipality(self, name: str, iso_country: str) -> tuple[float, float] | None:
        normalized = name.strip()
        # Prefer normalized City with coordinates
        city_qs = City.objects.active().filter(search_name__icontains=normalized.lower())
        if iso_country:
            city_qs = city_qs.filter(country__iso_code__iexact=iso_country)
        city = city_qs.exclude(latitude__isnull=True).exclude(longitude__isnull=True).first()
        if city and city.latitude is not None and city.longitude is not None:
            return float(city.latitude), float(city.longitude)

        # Fallback: airports by municipality
        ap_qs = Airport.objects.active().filter(municipality__icontains=normalized)
        if iso_country:
            ap_qs = ap_qs.filter(iso_country__iexact=iso_country)
        ap = ap_qs.first()
        if not ap:
            return None
        return float(ap.latitude_deg), float(ap.longitude_deg)
