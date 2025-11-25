"""Unit conversion utilities for distances and speeds.

Follow PRD requirements for km/mi support. Keep constants precise and
functions simple and dependency-free.
"""

from __future__ import annotations

KM_PER_MILE = 1.609344
MILES_PER_KM = 0.621371192237334


def km_to_mi(km: float) -> float:
    """Convert kilometers to miles.

    >>> round(km_to_mi(1.609344), 6)
    1.0
    """
    return km * MILES_PER_KM


def mi_to_km(mi: float) -> float:
    """Convert miles to kilometers.

    >>> round(mi_to_km(1.0), 6)
    1.609344
    """
    return mi * KM_PER_MILE
