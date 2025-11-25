"""Tests for normalized Country and City models."""

from django.db import IntegrityError
from django.test import TestCase

from apps.base.models import City, Country


class CountryModelTests(TestCase):
    """Verify Country normalization and helpers."""

    def test_country_normalization(self) -> None:
        country = Country.objects.create(iso_code="us", name=" United States ")
        self.assertEqual(country.iso_code, "US")
        self.assertEqual(country.search_name, "united states")
        self.assertTrue(country.slug.startswith("us-united-states"))

    def test_country_query_helpers(self) -> None:
        usa = Country.objects.create(iso_code="US", name="United States")
        Country.objects.create(iso_code="CA", name="Canada", active=False)

        self.assertEqual(list(Country.objects.active()), [usa])
        self.assertEqual(list(Country.objects.search("unit")), [usa])


class CityModelTests(TestCase):
    """Verify City normalization and constraints."""

    def setUp(self) -> None:
        self.country = Country.objects.create(iso_code="US", name="United States")

    def test_city_slug_and_search_name(self) -> None:
        city = City.objects.create(country=self.country, name="Denver")
        self.assertEqual(city.ascii_name, "Denver")
        self.assertEqual(city.search_name, "denver")
        self.assertTrue(city.slug.startswith("US-denver".lower()))

    def test_city_unique_per_country(self) -> None:
        City.objects.create(country=self.country, name="Dallas", ascii_name="Dallas")
        with self.assertRaises(IntegrityError):
            City.objects.create(country=self.country, name="DAllas", ascii_name="DAllas")

    def test_city_query_helpers(self) -> None:
        denver = City.objects.create(country=self.country, name="Denver")
        City.objects.create(country=self.country, name="Ghost Town", active=False)
        self.assertEqual(list(City.objects.active()), [denver])
        self.assertEqual(list(City.objects.search("den")), [denver])
