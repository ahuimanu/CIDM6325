from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from apps.airports.models import Airport
from apps.base.models import City, Country


class NearestAirportViewsTests(TestCase):
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

        self.airport_lax = Airport.objects.create(
            ident="KLAX",
            iata_code="LAX",
            name="Los Angeles International Airport",
            airport_type="large_airport",
            latitude_deg=33.9425,
            longitude_deg=-118.4081,
            iso_country="US",
            municipality="Los Angeles",
            country=self.us,
            active=True,
        )

    def test_page_get_200(self) -> None:
        url = reverse("airports:nearest")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Nearest Airports")

    def test_page_post_valid_shows_results(self) -> None:
        url = reverse("airports:nearest")
        resp = self.client.post(url, {"query": "32.9,-97.04", "unit": "km"})
        self.assertEqual(resp.status_code, 200)
        # Should list DFW at least
        self.assertContains(resp, "Dallas/Fort Worth International Airport")

    def test_json_valid(self) -> None:
        url = reverse("airports:nearest_json")
        resp = self.client.get(url, {"q": "32.9,-97.04", "unit": "km"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("results", data)
        self.assertIn("unit", data)
        self.assertEqual(data["unit"], "km")
        self.assertGreaterEqual(data["count"], 1)
        first = data["results"][0]
        self.assertIn("ident", first)
        self.assertIn("name", first)
        self.assertIn("distance", first)

    def test_json_invalid(self) -> None:
        url = reverse("airports:nearest_json")
        resp = self.client.get(url, {"q": "", "unit": "km"})
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertIn("errors", data)
