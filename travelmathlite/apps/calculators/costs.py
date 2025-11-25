"""
Cost-of-driving calculations and unit conversion helpers.

Implements fuel cost computation using distance, fuel economy, and fuel price;
includes conversions between common units.
"""

from __future__ import annotations

from typing import Final

from django.conf import settings

# Unit conversion constants
MILES_TO_KM: Final[float] = 1.60934
KM_TO_MILES: Final[float] = 0.621371
GALLON_TO_LITER: Final[float] = 3.78541
LITER_TO_GALLON: Final[float] = 1 / GALLON_TO_LITER
MPG_TO_L_PER_100KM_FACTOR: Final[float] = 235.214  # L/100km = 235.214 / MPG


def mpg_to_l_per_100km(mpg: float) -> float:
    """
    Convert miles-per-gallon (US) to liters per 100 kilometers.

    Formula: L/100km = 235.214 / MPG
    """
    if mpg <= 0:
        raise ValueError("MPG must be > 0")
    return MPG_TO_L_PER_100KM_FACTOR / mpg


def l_per_100km_to_mpg(l_per_100km: float) -> float:
    """
    Convert liters per 100 kilometers to miles-per-gallon (US).

    Formula: MPG = 235.214 / (L/100km)
    """
    if l_per_100km <= 0:
        raise ValueError("L/100km must be > 0")
    return MPG_TO_L_PER_100KM_FACTOR / l_per_100km


def gallons_to_liters(gallons: float) -> float:
    """Convert US gallons to liters."""
    if gallons < 0:
        raise ValueError("Gallons must be >= 0")
    return gallons * GALLON_TO_LITER


def liters_to_gallons(liters: float) -> float:
    """Convert liters to US gallons."""
    if liters < 0:
        raise ValueError("Liters must be >= 0")
    return liters * LITER_TO_GALLON


def calculate_fuel_cost(
    distance_km: float,
    fuel_economy_l_per_100km: float | None = None,
    fuel_price_per_liter: float | None = None,
    *,
    round_to_cents: bool = True,
) -> float:
    """
    Calculate total fuel cost for a trip.

    Cost formula:
        fuel_used_liters = (distance_km / 100) * fuel_economy_l_per_100km
        cost = fuel_used_liters * fuel_price_per_liter

    Defaults:
        - fuel_economy_l_per_100km: settings.FUEL_ECONOMY_L_PER_100KM
        - fuel_price_per_liter: settings.FUEL_PRICE_PER_LITER

    Returns a float; rounded to 2 decimals by default.
    """
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    eff_economy = fuel_economy_l_per_100km if fuel_economy_l_per_100km is not None else float(settings.FUEL_ECONOMY_L_PER_100KM)
    price = fuel_price_per_liter if fuel_price_per_liter is not None else float(settings.FUEL_PRICE_PER_LITER)

    fuel_used_l = (distance_km / 100.0) * eff_economy
    cost = fuel_used_l * price
    return round(cost, 2) if round_to_cents else cost
