from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.airports.models import Airport

UNITS = (
    ("km", "Kilometers"),
    ("miles", "Miles"),
)


@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float


CITY_COORDS = {
    # Common references to make city lookup deterministic without dataset
    "new york": Coordinates(40.7128, -74.0060),
    "los angeles": Coordinates(34.0522, -118.2437),
    "london": Coordinates(51.5074, -0.1278),
    "paris": Coordinates(48.8566, 2.3522),
}


def _parse_lat_lon(value: str) -> Coordinates | None:
    try:
        if "," not in value:
            return None
        lat_str, lon_str = [p.strip() for p in value.split(",", 1)]
        lat, lon = float(lat_str), float(lon_str)
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            raise ValidationError("Latitude must be -90..90 and longitude -180..180.")
        return Coordinates(lat, lon)
    except ValueError as e:
        raise ValidationError("Coordinates must be two numbers separated by a comma.") from e


def _lookup_iata(iata: str) -> Coordinates:
    code = iata.strip().upper()
    if len(code) != 3 or not code.isalpha():
        raise ValidationError("Invalid IATA code format.")
    ap = Airport.objects.filter(active=True, iata_code__iexact=code).first()
    if not ap:
        raise ValidationError(f"Unknown IATA code: {code}.")
    return Coordinates(ap.latitude_deg, ap.longitude_deg)


def _lookup_city(term: str) -> Coordinates:
    normalized = term.strip().lower()
    # Try airports.municipality first to avoid dependency on base.City fixtures
    ap = Airport.objects.filter(active=True, municipality__iexact=normalized).first()
    if ap:
        return Coordinates(ap.latitude_deg, ap.longitude_deg)
    if normalized in CITY_COORDS:
        return CITY_COORDS[normalized]
    raise ValidationError(f"Unknown city: {term}.")


class DistanceCalculatorForm(forms.Form):
    origin = forms.CharField(help_text="City name, IATA code, or 'lat,lon'.")
    destination = forms.CharField(help_text="City name, IATA code, or 'lat,lon'.")
    unit = forms.ChoiceField(choices=UNITS, initial="km")
    route_factor = forms.FloatField(
        min_value=0.5,
        max_value=3.0,
        help_text="Multiplier applied to straight-line distance to estimate driving distance.",
    )

    origin_coords: tuple[float, float]
    destination_coords: tuple[float, float]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["route_factor"].initial = float(getattr(settings, "ROUTE_FACTOR", 1.2))

    def _resolve(self, value: str) -> Coordinates:
        # Priority: lat,lon -> IATA -> city name
        value = value.strip()
        # Direct coordinates
        coords = _parse_lat_lon(value)
        if coords:
            return coords
        # IATA code
        if len(value) == 3 and value.isalpha():
            coords = _lookup_iata(value)
            if coords:
                return coords
        # City name via airports.municipality or fallback map
        return _lookup_city(value)

    def clean_origin(self) -> str:
        raw = self.cleaned_data["origin"].strip()
        coords = self._resolve(raw)
        self.origin_coords = (coords.lat, coords.lon)
        return raw

    def clean_destination(self) -> str:
        raw = self.cleaned_data["destination"].strip()
        coords = self._resolve(raw)
        self.destination_coords = (coords.lat, coords.lon)
        return raw


class CostCalculatorForm(DistanceCalculatorForm):
    fuel_economy_l_per_100km = forms.FloatField(
        min_value=0.1,
        help_text="Vehicle fuel economy in liters per 100 km.",
    )
    fuel_price_per_liter = forms.FloatField(
        min_value=0.0,
        help_text="Fuel price per liter.",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["fuel_economy_l_per_100km"].initial = float(getattr(settings, "FUEL_ECONOMY_L_PER_100KM", 7.5))
        self.fields["fuel_price_per_liter"].initial = float(getattr(settings, "FUEL_PRICE_PER_LITER", 1.50))
