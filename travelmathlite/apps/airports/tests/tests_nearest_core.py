"""Core tests for nearest-airport queryset helper.

Covers iso_country filtering, distance attachment, and limit behavior.
"""

from __future__ import annotations

from django.test import TestCase

from ..models import Airport


class NearestCoreTests(TestCase):
    def setUp(self) -> None:
        # Seed a few airports across two countries near the US/MX border area
        Airport.objects.create(
            ident="KELP",
            iata_code="ELP",
            name="El Paso International",
            airport_type="large_airport",
            latitude_deg=31.8072,
            longitude_deg=-106.3778,
            iso_country="US",
            active=True,
        )
        Airport.objects.create(
            ident="MMCS",
            iata_code="CJS",
            name="Ciudad Juárez Intl",
            airport_type="large_airport",
            latitude_deg=31.6361,
            longitude_deg=-106.429,
            iso_country="MX",
            active=True,
        )
        Airport.objects.create(
            ident="KLRU",
            iata_code="LRU",
            name="Las Cruces Intl",
            airport_type="medium_airport",
            latitude_deg=32.2894,
            longitude_deg=-106.9217,
            iso_country="US",
            active=True,
        )

    def test_nearest_attaches_distance_and_respects_limit(self) -> None:
        # Near El Paso coords
        lat, lon = 31.76, -106.49
        results = Airport.objects.nearest(lat, lon, limit=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(hasattr(results[0], "distance_km"))
        self.assertGreaterEqual(results[0].distance_km, 0.0)

    def test_iso_country_filter_limits_candidates(self) -> None:
        # Near El Paso coords
        lat, lon = 31.76, -106.49
        results_us = Airport.objects.nearest(lat, lon, limit=5, iso_country="US")
        self.assertTrue(all(a.iso_country.upper() == "US" for a in results_us))
        # Ensure at least one result exists and ordering by distance is stable
        self.assertGreaterEqual(len(results_us), 1)
        if len(results_us) > 1:
            self.assertLessEqual(results_us[0].distance_km, results_us[1].distance_km)

        # Without country filter, should include the MX airport among top results
        results_all = Airport.objects.nearest(lat, lon, limit=5)
        idents = {a.ident for a in results_all}
        self.assertIn("MMCS", idents)
