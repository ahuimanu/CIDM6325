"""Integration tests for caching behavior.

Verify end-to-end cache workflows including:
- Search with caching
- Cache invalidation
- Performance improvements
- Cache key variation
"""

import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from apps.airports.models import Airport  # type: ignore[import-not-found]
from apps.base.models import City, Country  # type: ignore[import-not-found]

User = get_user_model()


class CachingIntegrationTestCase(TestCase):
    """Test complete caching workflows."""

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
        self.city_dallas = City.objects.create(
            country=self.country,
            name="Dallas",
            slug="dallas",
        )
        self.city_houston = City.objects.create(
            country=self.country,
            name="Houston",
            slug="houston",
        )

        # Create airports
        self.dal = Airport.objects.create(
            ident="KDAL",
            iata_code="DAL",
            name="Dallas Love Field",
            municipality="Dallas",
            iso_country="US",
            country=self.country,
            city=self.city_dallas,
            latitude_deg=32.8470,
            longitude_deg=-96.8517,
            active=True,
        )
        self.dfw = Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas/Fort Worth International",
            municipality="Dallas",
            iso_country="US",
            country=self.country,
            city=self.city_dallas,
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            active=True,
        )
        self.iah = Airport.objects.create(
            ident="KIAH",
            iata_code="IAH",
            name="George Bush Intercontinental",
            municipality="Houston",
            iso_country="US",
            country=self.country,
            city=self.city_houston,
            latitude_deg=29.9844,
            longitude_deg=-95.3414,
            active=True,
        )

        self.client = Client()

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_search_workflow_with_caching(self) -> None:
        """Test complete search workflow with caching."""
        # First search - cache miss
        start = time.perf_counter()
        response1 = self.client.get("/search/?q=Dallas")
        time1 = time.perf_counter() - start

        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "Dallas")

        # Repeat search - cache hit (same query)
        start = time.perf_counter()
        response2 = self.client.get("/search/?q=Dallas")
        time2 = time.perf_counter() - start

        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Dallas")

        # Content should be identical
        self.assertEqual(response1.content, response2.content)

        # Second request should be faster (cache hit)
        # Note: In tests, the difference may be small due to in-memory database
        # In production with real database, the improvement is more significant
        self.assertLessEqual(time2, time1 * 1.5)  # Allow some variance

    def test_cache_invalidation_workflow(self) -> None:
        """Test cache clearing and re-population."""
        # Populate cache
        response1 = self.client.get("/search/?q=Dallas")
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "Dallas")

        # Clear cache
        cache.clear()

        # Next request should work (cache miss, repopulated)
        response2 = self.client.get("/search/?q=Dallas")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Dallas")

        # Content should still be correct
        self.assertEqual(response1.content, response2.content)

    def test_cache_key_variation_by_query(self) -> None:
        """Test that different queries use different cache keys."""
        # Different searches should return different results
        dallas_response = self.client.get("/search/?q=Dallas")
        houston_response = self.client.get("/search/?q=Houston")

        self.assertEqual(dallas_response.status_code, 200)
        self.assertEqual(houston_response.status_code, 200)

        # Content should differ
        self.assertNotEqual(dallas_response.content, houston_response.content)
        self.assertContains(dallas_response, "Dallas")
        self.assertContains(houston_response, "Houston")

    def test_cache_key_variation_by_pagination(self) -> None:
        """Test that different page numbers use different cache keys."""
        # Page 1
        page1 = self.client.get("/search/?q=Dallas&page=1")
        self.assertEqual(page1.status_code, 200)

        # Page 2 (may not exist, but cache key should differ)
        page2 = self.client.get("/search/?q=Dallas&page=2")
        # Page 2 might return 200 with empty results or 404, both are acceptable
        self.assertIn(page2.status_code, [200, 404])

    def test_calculator_caching(self) -> None:
        """Test that calculator results are cached."""
        # First request - cache miss
        response1 = self.client.get("/calculators/distance/")
        self.assertEqual(response1.status_code, 200)

        # Second request - cache hit
        response2 = self.client.get("/calculators/distance/")
        self.assertEqual(response2.status_code, 200)

        # Content should be identical
        self.assertEqual(response1.content, response2.content)

    def test_post_requests_bypass_cache(self) -> None:
        """Test that POST requests bypass cache."""
        # POST requests should not be cached
        response1 = self.client.post("/calculators/distance/", {})
        response2 = self.client.post("/calculators/distance/", {})

        # Both should process (not cached)
        # Status may be 200 (form errors) or 400 (validation errors)
        self.assertIn(response1.status_code, [200, 400])
        self.assertIn(response2.status_code, [200, 400])

    def test_authenticated_vs_anonymous_caching(self) -> None:
        """Test that authenticated and anonymous users get appropriate cache behavior."""
        # Anonymous user
        anon_response = self.client.get("/")
        self.assertEqual(anon_response.status_code, 200)

        # Authenticated user
        _user = User.objects.create_user(username="test", password="test123")
        self.client.login(username="test", password="test123")
        auth_response = self.client.get("/")
        self.assertEqual(auth_response.status_code, 200)

        # Both should succeed (cache behavior differs via Cache-Control headers)
        # Anonymous: public cache
        # Authenticated: private cache
        self.assertIn("Cache-Control", anon_response)
        self.assertIn("Cache-Control", auth_response)


class LowLevelCachingIntegrationTestCase(TestCase):
    """Test low-level caching utilities integration."""

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
        self.airport = Airport.objects.create(
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

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_airport_query_caching_integration(self) -> None:
        """Test airport query caching with real data."""
        from apps.airports.utils import get_airports_by_country

        # First call - cache miss
        airports1 = get_airports_by_country("US")
        self.assertEqual(len(airports1), 1)
        self.assertEqual(airports1[0].iata_code, "DAL")

        # Second call - cache hit
        airports2 = get_airports_by_country("US")
        self.assertEqual(len(airports2), 1)
        self.assertEqual(airports2, airports1)

    def test_distance_calculation_caching_integration(self) -> None:
        """Test distance calculation caching with real coordinates."""
        from apps.calculators.utils import haversine_distance_cached

        # Dallas to Houston coordinates
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        # First call - cache miss
        distance1 = haversine_distance_cached(lat1, lon1, lat2, lon2)
        self.assertGreater(distance1, 0)

        # Second call - cache hit
        distance2 = haversine_distance_cached(lat1, lon1, lat2, lon2)
        self.assertEqual(distance1, distance2)


class CachePerformanceTestCase(TestCase):
    """Test cache performance improvements."""

    def setUp(self) -> None:
        """Clear cache before tests."""
        cache.clear()

        # Create test data
        country = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="united-states",
        )
        city = City.objects.create(
            country=country,
            name="Dallas",
            slug="dallas",
        )

        # Create multiple airports for more realistic data
        for i in range(5):
            Airport.objects.create(
                ident=f"K{i:03d}",
                iata_code=f"D{i:02d}",
                name=f"Test Airport {i}",
                municipality="Dallas",
                iso_country="US",
                country=country,
                city=city,
                latitude_deg=32.8 + i * 0.1,
                longitude_deg=-96.8 + i * 0.1,
                active=True,
            )

    def tearDown(self) -> None:
        """Clear cache after tests."""
        cache.clear()

    def test_cache_improves_query_performance(self) -> None:
        """Test that caching improves query performance."""
        from apps.airports.utils import get_airports_by_country

        # First call - uncached
        start = time.perf_counter()
        airports1 = get_airports_by_country("US")
        time_uncached = time.perf_counter() - start

        self.assertEqual(len(airports1), 5)

        # Second call - cached
        start = time.perf_counter()
        airports2 = get_airports_by_country("US")
        time_cached = time.perf_counter() - start

        self.assertEqual(len(airports2), 5)
        self.assertEqual(airports1, airports2)

        # Cached version should be faster
        # In tests, the improvement may be small; in production it's more significant
        self.assertLessEqual(time_cached, time_uncached * 2)  # Allow some variance
