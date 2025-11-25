from __future__ import annotations

from django.test import TestCase

from apps.airports.forms import NearestAirportForm
from apps.airports.models import Airport
from apps.base.models import City, Country


class NearestAirportFormTests(TestCase):
    def setUp(self) -> None:
        self.us = Country.objects.create(iso_code="US", name="United States", search_name="united states", slug="us")
        self.mx = Country.objects.create(iso_code="MX", name="Mexico", search_name="mexico", slug="mx")

        self.dallas = City.objects.create(
            country=self.us,
            name="Dallas",
            ascii_name="Dallas",
            search_name="dallas",
            slug="us-dallas",
            latitude=32.7767,
            longitude=-96.7970,
        )

        self.airport_dfw = Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas/Fort Worth International Airport",
            airport_type="large_airport",
            latitude_deg=32.8998,
            longitude_deg=-97.0403,
            iso_country="US",
            municipality="Dallas",
            country=self.us,
            city=self.dallas,
            active=True,
        )

        self.airport_mex = Airport.objects.create(
            ident="MMMX",
            iata_code="MEX",
            name="Mexico City International Airport",
            airport_type="large_airport",
            latitude_deg=19.4361,
            longitude_deg=-99.0719,
            iso_country="MX",
            municipality="Mexico City",
            country=self.mx,
            active=True,
        )

    def test_direct_coordinates_valid(self) -> None:
        form = NearestAirportForm(data={"query": "32.9,-97.04"})
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.resolved_coords)
        lat, lon = form.resolved_coords or (0.0, 0.0)
        self.assertAlmostEqual(lat, 32.9, places=3)
        self.assertAlmostEqual(lon, -97.04, places=3)

    def test_direct_coordinates_invalid_range(self) -> None:
        form = NearestAirportForm(data={"query": "-95,10"})
        self.assertFalse(form.is_valid())
        self.assertIn("query", form.errors)

        form2 = NearestAirportForm(data={"query": "10, 190"})
        self.assertFalse(form2.is_valid())
        self.assertIn("query", form2.errors)

    def test_iata_resolves_coords(self) -> None:
        form = NearestAirportForm(data={"query": "dfw"})
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.resolved_coords)
        lat, lon = form.resolved_coords or (0.0, 0.0)
        self.assertAlmostEqual(lat, self.airport_dfw.latitude_deg, places=3)
        self.assertAlmostEqual(lon, self.airport_dfw.longitude_deg, places=3)

    def test_iata_filters_by_iso_country(self) -> None:
        # Create another airport with same IATA in MX to exercise country filter
        Airport.objects.create(
            ident="TEST1",
            iata_code="DFW",
            name="Fake DFW MX",
            airport_type="medium_airport",
            latitude_deg=20.0,
            longitude_deg=-99.0,
            iso_country="MX",
            municipality="Test City",
            country=self.mx,
            active=True,
        )

        # With MX, should not resolve to US DFW
        form_mx = NearestAirportForm(data={"query": "DFW", "iso_country": "mx"})
        self.assertTrue(form_mx.is_valid())
        lat_mx, _ = form_mx.resolved_coords or (None, None)
        self.assertAlmostEqual(lat_mx or 0.0, 20.0, places=3)

        # With US (or unspecified), resolves to US DFW
        form_us = NearestAirportForm(data={"query": "DFW", "iso_country": "US"})
        self.assertTrue(form_us.is_valid())
        lat_us, _ = form_us.resolved_coords or (0.0, 0.0)
        self.assertAlmostEqual(lat_us, self.airport_dfw.latitude_deg, places=3)

    def test_city_resolves_via_city_model(self) -> None:
        form = NearestAirportForm(data={"query": "Dallas"})
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.resolved_coords)
        lat, lon = form.resolved_coords or (0.0, 0.0)
        self.assertAlmostEqual(lat, self.dallas.latitude or 0.0, places=3)
        self.assertAlmostEqual(lon, self.dallas.longitude or 0.0, places=3)

    def test_city_resolves_via_municipality_fallback(self) -> None:
        # Remove city coordinates to force municipality fallback
        self.dallas.latitude = None
        self.dallas.longitude = None
        self.dallas.save()

        form = NearestAirportForm(data={"query": "Dallas"})
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.resolved_coords)
        lat, lon = form.resolved_coords or (0.0, 0.0)
        self.assertAlmostEqual(lat, self.airport_dfw.latitude_deg, places=3)
        self.assertAlmostEqual(lon, self.airport_dfw.longitude_deg, places=3)

    def test_defaults_unit_and_limit(self) -> None:
        form = NearestAirportForm(data={"query": "32.0, -97.0"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("unit"), "km")
        self.assertEqual(form.cleaned_data.get("limit"), 3)

    def test_iso_country_normalization(self) -> None:
        form = NearestAirportForm(data={"query": "DFW", "iso_country": "us"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("iso_country"), "US")

    def test_iata_unknown_errors(self) -> None:
        form = NearestAirportForm(data={"query": "ZZZ"})
        self.assertFalse(form.is_valid())
        self.assertIn("query", form.errors)
