"""Integration tests for linking airports to normalized core models."""

from __future__ import annotations

import csv
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from apps.airports.models import Airport
from apps.airports.services import AirportLocationIntegrator
from apps.base.models import City, Country


class AirportLocationIntegrationTests(TestCase):
    """Verify importer links Airports to Country/City and QuerySet helpers work."""

    def _create_csv(self, rows: list[dict[str, str]]) -> Path:
        temp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="")
        writer = csv.DictWriter(temp, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        temp.close()
        return Path(temp.name)

    def test_location_integrator_creates_country_and_city(self) -> None:
        integrator = AirportLocationIntegrator()
        link = integrator.link_location(
            iso_country="us",
            municipality="Denver",
            latitude=39.7,
            longitude=-104.9,
        )
        self.assertIsNotNone(link.country)
        self.assertEqual(link.country.iso_code, "US")
        self.assertTrue(link.created_country)
        self.assertIsNotNone(link.city)
        self.assertEqual(link.city.name, "Denver")

    def test_import_command_links_airports(self) -> None:
        csv_file = self._create_csv(
            [
                {
                    "id": "1",
                    "ident": "TEST1",
                    "type": "large_airport",
                    "name": "Test International",
                    "latitude_deg": "39.8561",
                    "longitude_deg": "-104.6737",
                    "elevation_ft": "5434",
                    "iso_country": "US",
                    "iso_region": "US-CO",
                    "municipality": "Denver",
                    "iata_code": "TST",
                }
            ]
        )

        try:
            out = StringIO()
            call_command("import_airports", file=str(csv_file), stdout=out)
        finally:
            csv_file.unlink()

        airport = Airport.objects.get(ident="TEST1")
        self.assertIsNotNone(airport.country)
        self.assertEqual(airport.country.iso_code, "US")
        self.assertIsNotNone(airport.city)
        self.assertEqual(airport.city.name, "Denver")

    def test_nearest_queryset_helper_orders_results(self) -> None:
        usa = Country.objects.create(iso_code="US", name="United States")
        denver = City.objects.create(country=usa, name="Denver", latitude=39.74, longitude=-104.99)
        chicago = City.objects.create(country=usa, name="Chicago", latitude=41.88, longitude=-87.63)
        nyc = City.objects.create(country=usa, name="New York", latitude=40.71, longitude=-74.00)

        Airport.objects.create(
            ident="DEN",
            iata_code="DEN",
            name="Denver International",
            airport_type="large_airport",
            latitude_deg=39.8561,
            longitude_deg=-104.6737,
            iso_country="US",
            country=usa,
            city=denver,
        )
        Airport.objects.create(
            ident="ORD",
            iata_code="ORD",
            name="O'Hare International",
            airport_type="large_airport",
            latitude_deg=41.9742,
            longitude_deg=-87.9073,
            iso_country="US",
            country=usa,
            city=chicago,
        )
        Airport.objects.create(
            ident="JFK",
            iata_code="JFK",
            name="John F. Kennedy International",
            airport_type="large_airport",
            latitude_deg=40.6413,
            longitude_deg=-73.7781,
            iso_country="US",
            country=usa,
            city=nyc,
        )

        nearest = Airport.objects.nearest(39.7392, -104.9903, limit=2)
        self.assertEqual(len(nearest), 2)
        self.assertEqual(nearest[0].ident, "DEN")
        self.assertEqual(nearest[1].ident, "ORD")
        self.assertTrue(hasattr(nearest[0], "distance_km"))


class AirportQuerySetSearchTests(TestCase):
    """Ensure Airport search helper respects normalized data."""

    def setUp(self) -> None:
        country = Country.objects.create(iso_code="US", name="United States")
        city = City.objects.create(country=country, name="Austin")
        self.airport = Airport.objects.create(
            ident="AUS",
            iata_code="AUS",
            name="Austin Bergstrom",
            airport_type="large_airport",
            latitude_deg=30.1975,
            longitude_deg=-97.6664,
            iso_country="US",
            country=country,
            city=city,
            municipality="Austin",
        )

    def test_search_matches_normalized_fields(self) -> None:
        results = Airport.objects.search("Austin")
        self.assertIn(self.airport, results)
        results_code = Airport.objects.search("AUS")
        self.assertIn(self.airport, results_code)
