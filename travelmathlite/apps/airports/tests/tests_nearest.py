"""Comprehensive tests for nearest-airport feature: ordering, units, filters, endpoints, and performance.

Addresses PRD §4 F-002, §7 NF-001.
"""

from __future__ import annotations

import time

from django.test import TestCase
from django.urls import reverse

from ...base.models import Country
from ...base.utils.units import km_to_mi
from ..models import Airport


class NearestOrderingAndUnitsTests(TestCase):
    """Test ordering stability, distance attachment, and unit conversions."""

    def setUp(self) -> None:
        # Seed 5-10 airports around Dallas area (32.7767, -96.7970)
        # These will be at varying distances to test ordering
        self.us = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="us",
        )

        self.airports = [
            Airport.objects.create(
                ident="KDFW",
                iata_code="DFW",
                name="Dallas Fort Worth Intl",
                airport_type="large_airport",
                latitude_deg=32.8968,
                longitude_deg=-97.0380,
                iso_country="US",
                country=self.us,
                active=True,
            ),
            Airport.objects.create(
                ident="KDAL",
                iata_code="DAL",
                name="Dallas Love Field",
                airport_type="medium_airport",
                latitude_deg=32.8471,
                longitude_deg=-96.8518,
                iso_country="US",
                country=self.us,
                active=True,
            ),
            Airport.objects.create(
                ident="KADS",
                iata_code="ADS",
                name="Addison Airport",
                airport_type="small_airport",
                latitude_deg=32.9686,
                longitude_deg=-96.8364,
                iso_country="US",
                country=self.us,
                active=True,
            ),
            Airport.objects.create(
                ident="KFTW",
                iata_code="FTW",
                name="Fort Worth Meacham",
                airport_type="medium_airport",
                latitude_deg=32.8198,
                longitude_deg=-97.3624,
                iso_country="US",
                country=self.us,
                active=True,
            ),
            Airport.objects.create(
                ident="KAFW",
                iata_code="AFW",
                name="Fort Worth Alliance",
                airport_type="medium_airport",
                latitude_deg=32.9876,
                longitude_deg=-97.3188,
                iso_country="US",
                country=self.us,
                active=True,
            ),
        ]

    def test_top_3_ordered_by_distance(self) -> None:
        """Verify top 3 results are ordered by computed distance (INV-1)."""
        lat, lon = 32.7767, -96.7970  # Dallas center
        results = Airport.objects.nearest(lat, lon, limit=3)

        self.assertEqual(len(results), 3)
        # Each should have distance_km attached
        for airport in results:
            self.assertTrue(hasattr(airport, "distance_km"))
            self.assertIsInstance(airport.distance_km, float)
            self.assertGreaterEqual(airport.distance_km, 0.0)

        # Assert ascending distance order (INV-1)
        self.assertLessEqual(results[0].distance_km, results[1].distance_km)
        self.assertLessEqual(results[1].distance_km, results[2].distance_km)

    def test_km_to_mi_conversion_correct(self) -> None:
        """Verify km/mi conversions match expected values."""
        lat, lon = 32.7767, -96.7970
        results_km = Airport.objects.nearest(lat, lon, limit=3, unit="km")
        results_mi = Airport.objects.nearest(lat, lon, limit=3, unit="mi")

        # Both should have distance_km
        self.assertTrue(hasattr(results_km[0], "distance_km"))
        self.assertTrue(hasattr(results_mi[0], "distance_km"))

        # mi results should also have distance_mi
        self.assertTrue(hasattr(results_mi[0], "distance_mi"))

        # Verify conversion accuracy for each result
        for i in range(len(results_mi)):
            km = results_mi[i].distance_km
            mi = results_mi[i].distance_mi
            expected_mi = km_to_mi(km)
            self.assertAlmostEqual(mi, expected_mi, places=4)

    def test_country_filter_narrows_results(self) -> None:
        """Verify iso_country filter limits candidates to specified country."""
        # Add one Mexican airport near the border
        self.mx = Country.objects.create(
            iso_code="MX",
            name="Mexico",
            search_name="mexico",
            slug="mx",
        )
        Airport.objects.create(
            ident="MMCS",
            iata_code="CJS",
            name="Ciudad Juárez Intl",
            airport_type="large_airport",
            latitude_deg=31.6361,
            longitude_deg=-106.4290,
            iso_country="MX",
            country=self.mx,
            active=True,
        )

        # Search near El Paso (31.76, -106.49) which is close to both US and MX airports
        lat, lon = 31.76, -106.49

        # Without filter - should include MX airport
        results_all = Airport.objects.nearest(lat, lon, limit=5)
        countries_all = {a.iso_country for a in results_all}
        self.assertIn("MX", countries_all)

        # With US filter - should exclude MX airport
        results_us = Airport.objects.nearest(lat, lon, limit=5, iso_country="US")
        countries_us = {a.iso_country for a in results_us}
        self.assertNotIn("MX", countries_us)
        self.assertTrue(all(c == "US" for c in countries_us))


class NearestEndpointsTests(TestCase):
    """Test JSON and HTML/HTMX endpoints for nearest airports."""

    def setUp(self) -> None:
        self.us = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="us",
        )
        Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas Fort Worth Intl",
            airport_type="large_airport",
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            iso_country="US",
            country=self.us,
            active=True,
        )
        Airport.objects.create(
            ident="KDAL",
            iata_code="DAL",
            name="Dallas Love Field",
            airport_type="medium_airport",
            latitude_deg=32.8471,
            longitude_deg=-96.8518,
            iso_country="US",
            country=self.us,
            active=True,
        )

    def test_json_endpoint_returns_expected_shape(self) -> None:
        """Verify JSON endpoint returns {results, count, unit}."""
        url = reverse("airports:nearest_json")
        resp = self.client.get(url, {"q": "32.8968,-97.0380", "unit": "km", "limit": "3"})

        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Check required keys
        self.assertIn("results", data)
        self.assertIn("count", data)
        self.assertIn("unit", data)

        # Validate structure
        self.assertIsInstance(data["results"], list)
        self.assertIsInstance(data["count"], int)
        self.assertEqual(data["unit"], "km")
        self.assertGreaterEqual(data["count"], 1)

        # Check first result structure
        if len(data["results"]) > 0:
            first = data["results"][0]
            self.assertIn("ident", first)
            self.assertIn("iata", first)
            self.assertIn("name", first)
            self.assertIn("distance", first)

    def test_json_endpoint_with_invalid_query_returns_400(self) -> None:
        """Verify JSON endpoint returns 400 with errors for invalid input."""
        url = reverse("airports:nearest_json")
        resp = self.client.get(url, {"q": "", "unit": "km"})

        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertIn("errors", data)

    def test_html_view_renders_full_page_on_standard_post(self) -> None:
        """Verify standard POST returns full HTML page with results."""
        url = reverse("airports:nearest")
        resp = self.client.post(url, {"query": "32.8968,-97.0380", "unit": "km", "limit": "3"})

        self.assertEqual(resp.status_code, 200)
        # Should contain full page elements
        self.assertContains(resp, "<!DOCTYPE html>", html=True)
        self.assertContains(resp, "Dallas Fort Worth Intl")

    def test_htmx_post_returns_partial_template_only(self) -> None:
        """Verify HTMX POST returns only the results partial, not full HTML."""
        url = reverse("airports:nearest")
        resp = self.client.post(
            url,
            {"query": "32.8968,-97.0380", "unit": "km", "limit": "3"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # Should NOT contain full page doctype
        self.assertNotIn("<!DOCTYPE html>", content)

        # Should contain results content
        self.assertIn("Dallas Fort Worth Intl", content)

        # Should be using the partial template structure
        self.assertIn("<h2>", content)  # Results heading from partial

    def test_htmx_invalid_form_returns_error_message_in_partial(self) -> None:
        """Verify HTMX POST with invalid form returns error in partial."""
        url = reverse("airports:nearest")
        resp = self.client.post(
            url,
            {"query": "", "unit": "km"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # Should not contain full page doctype
        self.assertNotIn("<!DOCTYPE html>", content)

        # Should indicate no results
        self.assertIn("No results found", content)


class NearestPerformanceTests(TestCase):
    """Test performance targets for nearest() on sample fixtures."""

    def setUp(self) -> None:
        # Seed 10 airports to simulate realistic fixture size
        self.us = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="us",
        )

        coords = [
            (32.8968, -97.0380, "KDFW", "DFW", "Dallas Fort Worth Intl"),
            (32.8471, -96.8518, "KDAL", "DAL", "Dallas Love Field"),
            (32.9686, -96.8364, "KADS", "ADS", "Addison Airport"),
            (32.8198, -97.3624, "KFTW", "FTW", "Fort Worth Meacham"),
            (32.9876, -97.3188, "KAFW", "AFW", "Fort Worth Alliance"),
            (33.9425, -118.4081, "KLAX", "LAX", "Los Angeles Intl"),
            (41.9786, -87.9048, "KORD", "ORD", "Chicago O'Hare"),
            (40.6413, -73.7781, "KJFK", "JFK", "John F Kennedy Intl"),
            (42.3643, -71.0052, "KBOS", "BOS", "Boston Logan"),
            (47.4502, -122.3088, "KSEA", "SEA", "Seattle-Tacoma Intl"),
        ]

        for lat, lon, ident, iata, name in coords:
            Airport.objects.create(
                ident=ident,
                iata_code=iata,
                name=name,
                airport_type="large_airport",
                latitude_deg=lat,
                longitude_deg=lon,
                iso_country="US",
                country=self.us,
                active=True,
            )

    def test_nearest_timing_on_small_fixture(self) -> None:
        """Measure and log simple duration for nearest() call.

        Target: p95 < 300ms (local hint only, not enforced in CI).
        """
        lat, lon = 32.7767, -96.7970

        # Warm-up call to ensure DB connections are established
        Airport.objects.nearest(lat, lon, limit=3)

        # Timed calls
        timings = []
        for _ in range(10):
            start = time.perf_counter()
            results = Airport.objects.nearest(lat, lon, limit=3)
            elapsed = time.perf_counter() - start
            timings.append(elapsed * 1000)  # Convert to milliseconds

            # Sanity check: should return results
            self.assertGreaterEqual(len(results), 1)

        # Calculate percentiles
        timings_sorted = sorted(timings)
        p50 = timings_sorted[len(timings_sorted) // 2]
        p95 = timings_sorted[int(len(timings_sorted) * 0.95)]
        avg = sum(timings) / len(timings)

        # Log timing evidence (visible in test output)
        print("\n[Timing Evidence] nearest() on 10-airport fixture:")
        print(f"  avg: {avg:.2f}ms, p50: {p50:.2f}ms, p95: {p95:.2f}ms")

        # Generous threshold for CI safety - just ensure it's not absurdly slow
        # Target p95 < 300ms; we assert < 1000ms to avoid flakes
        self.assertLess(
            p95,
            1000,
            f"p95 timing {p95:.2f}ms exceeds generous CI threshold (target: <300ms local)",
        )
