"""Tests for distance unit support (km and mi)."""

from __future__ import annotations

from django.test import TestCase

from apps.airports.models import Airport
from apps.base.utils.units import km_to_mi


class DistanceUnitsTests(TestCase):
    def setUp(self) -> None:
        # Seed a couple of airports near Dallas
        Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas Fort Worth International Airport",
            airport_type="large_airport",
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            iso_country="US",
        )
        Airport.objects.create(
            ident="KDAL",
            iata_code="DAL",
            name="Dallas Love Field",
            airport_type="medium_airport",
            latitude_deg=32.8471,
            longitude_deg=-96.8518,
            iso_country="US",
        )

    def test_nearest_attaches_distance_km(self) -> None:
        results = Airport.objects.nearest(32.8968, -97.0380, limit=2)
        self.assertTrue(len(results) >= 1)
        self.assertTrue(hasattr(results[0], "distance_km"))

    def test_nearest_attaches_distance_mi_when_requested(self) -> None:
        results = Airport.objects.nearest(32.8968, -97.0380, limit=2, unit="mi")
        self.assertTrue(hasattr(results[0], "distance_km"))
        self.assertTrue(hasattr(results[0], "distance_mi"))

        # Validate conversion for the second airport (~11.3 km ≈ 7.0 mi)
        if len(results) > 1:
            km = results[1].distance_km
            mi = results[1].distance_mi
            self.assertAlmostEqual(mi, km_to_mi(km), places=4)
