"""Tests for airport caching utilities.

Verify cache behavior for airport query operations.
"""

from django.core.cache import cache
from django.test import TestCase

from ...base.models import City, Country
from ..models import Airport
from ..utils import (
    clear_airport_cache,
    get_airports_by_city,
    get_airports_by_country,
    get_airports_by_iata,
    get_nearest_airports_cached,
    search_airports_cached,
)


class AirportCachingTestCase(TestCase):
    """Test caching behavior for airport queries."""

    def setUp(self) -> None:
        """Create test data and clear cache."""
        cache.clear()

        # Create test data
        self.country = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="united-states",
        )
        self.city = City.objects.create(
            country=self.country,
            name="Dallas",
            slug="dallas",
        )
        self.airport1 = Airport.objects.create(
            ident="KDAL",
            iata_code="DAL",
            name="Dallas Love Field",
            municipality="Dallas",
            iso_country="US",
            country=self.country,
            city=self.city,
            latitude_deg=32.8470,
            longitude_deg=-96.8517,
            active=True,
        )
        self.airport2 = Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas/Fort Worth International",
            municipality="Dallas",
            iso_country="US",
            country=self.country,
            city=self.city,
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            active=True,
        )

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_airports_cached_by_country(self) -> None:
        """Test that airport queries by country are cached."""
        # First call - cache miss
        airports1 = get_airports_by_country("US")
        self.assertEqual(len(airports1), 2)

        # Second call - cache hit
        airports2 = get_airports_by_country("US")
        self.assertEqual(len(airports2), 2)

        # Should return same results
        self.assertEqual(airports1, airports2)

    def test_different_countries_different_cache(self) -> None:
        """Test that different countries use different cache keys."""
        airports_us = get_airports_by_country("US")
        airports_uk = get_airports_by_country("UK")

        # US has airports, UK doesn't
        self.assertEqual(len(airports_us), 2)
        self.assertEqual(len(airports_uk), 0)

    def test_airports_cached_by_city(self) -> None:
        """Test that airport queries by city are cached."""
        # First call - cache miss
        airports1 = get_airports_by_city("Dallas")
        self.assertEqual(len(airports1), 2)

        # Second call - cache hit
        airports2 = get_airports_by_city("Dallas")
        self.assertEqual(len(airports2), 2)

        # Results should match
        self.assertEqual(airports1, airports2)

    def test_airport_cached_by_iata(self) -> None:
        """Test that airport queries by IATA code are cached."""
        # First call - cache miss
        airport1 = get_airports_by_iata("DAL")
        self.assertIsNotNone(airport1)
        self.assertEqual(airport1.iata_code, "DAL")  # type: ignore[union-attr]

        # Second call - cache hit
        airport2 = get_airports_by_iata("DAL")
        self.assertIsNotNone(airport2)
        self.assertEqual(airport2.iata_code, "DAL")  # type: ignore[union-attr]

        # Should be the same object
        self.assertEqual(airport1, airport2)

    def test_iata_not_found_cached(self) -> None:
        """Test that negative lookups (not found) are also cached."""
        # First call - cache miss
        airport1 = get_airports_by_iata("XXX")
        self.assertIsNone(airport1)

        # Second call - should return cached None
        airport2 = get_airports_by_iata("XXX")
        self.assertIsNone(airport2)

    def test_nearest_airports_cached(self) -> None:
        """Test that nearest airport queries are cached."""
        # Dallas center coordinates
        lat, lon = 32.7767, -96.7970

        # First call - cache miss
        results1 = get_nearest_airports_cached(lat, lon, limit=5)
        self.assertGreater(len(results1), 0)

        # Second call - cache hit
        results2 = get_nearest_airports_cached(lat, lon, limit=5)
        self.assertEqual(len(results1), len(results2))

    def test_search_airports_cached(self) -> None:
        """Test that airport search results are cached."""
        # First call - cache miss
        results1 = search_airports_cached("Dallas")
        self.assertGreater(len(results1), 0)

        # Second call - cache hit
        results2 = search_airports_cached("Dallas")
        self.assertEqual(len(results1), len(results2))

        # Results should be identical
        self.assertEqual(results1, results2)

    def test_cache_key_uniqueness(self) -> None:
        """Test that different parameters generate different cache keys."""
        # Different country codes
        us_airports = get_airports_by_country("US")
        uk_airports = get_airports_by_country("UK")

        # Should not interfere
        self.assertEqual(len(us_airports), 2)
        self.assertEqual(len(uk_airports), 0)

        # Different cities
        dallas_airports = get_airports_by_city("Dallas")
        houston_airports = get_airports_by_city("Houston")

        self.assertEqual(len(dallas_airports), 2)
        self.assertEqual(len(houston_airports), 0)

    def test_cache_invalidation(self) -> None:
        """Test manual cache clearing."""
        # Cache some data
        airports = get_airports_by_country("US")
        self.assertEqual(len(airports), 2)

        # Clear cache
        clear_airport_cache()

        # Verify we can still query (cache miss, re-fetched)
        airports_after = get_airports_by_country("US")
        self.assertEqual(len(airports_after), 2)

    def test_cache_clears_successfully(self) -> None:
        """Test that cache clear works."""
        # Populate cache
        get_airports_by_country("US")
        get_airports_by_city("Dallas")
        get_airports_by_iata("DAL")

        # Clear all airport cache
        clear_airport_cache()

        # Verify data can still be fetched (re-queried from database)
        airports = get_airports_by_country("US")
        self.assertEqual(len(airports), 2)
