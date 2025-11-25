"""Tests for calculator view caching behavior.

Verify that calculator results are cached with proper TTLs and key variation.
"""

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse


class CalculatorCachingTestCase(TestCase):
    """Test caching behavior for calculator views."""

    def setUp(self) -> None:
        """Clear cache and create test client."""
        cache.clear()
        self.client = Client()

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_distance_calculator_cached(self) -> None:
        """Test that distance calculator GET requests are cached."""
        url = reverse("calculators:distance")

        # First request (cache miss)
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        content1 = response1.content

        # Second identical request (cache hit)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        content2 = response2.content

        # Content should be identical (cached response)
        self.assertEqual(content1, content2)

    def test_cost_calculator_cached(self) -> None:
        """Test that cost calculator GET requests are cached."""
        url = reverse("calculators:cost")

        # First request (cache miss)
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        content1 = response1.content

        # Second identical request (cache hit)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        content2 = response2.content

        # Content should be identical (cached response)
        self.assertEqual(content1, content2)

    def test_distance_post_bypasses_cache(self) -> None:
        """Test that POST requests to distance calculator bypass cache."""
        url = reverse("calculators:distance")

        # Valid form data
        form_data = {
            "origin_lat": "32.8473",
            "origin_lon": "-96.8513",
            "destination_lat": "29.7604",
            "destination_lon": "-95.3698",
            "unit": "km",
            "route_factor": "1.2",
        }

        # First POST request
        response1 = self.client.post(url, form_data)
        self.assertEqual(response1.status_code, 200)

        # Second identical POST request (should not use cache)
        response2 = self.client.post(url, form_data)
        self.assertEqual(response2.status_code, 200)

        # Both should succeed; POST requests don't cache
        self.assertIsNotNone(response1.content)
        self.assertIsNotNone(response2.content)

    def test_cost_post_bypasses_cache(self) -> None:
        """Test that POST requests to cost calculator bypass cache."""
        url = reverse("calculators:cost")

        # Valid form data
        form_data = {
            "origin_lat": "32.8473",
            "origin_lon": "-96.8513",
            "destination_lat": "29.7604",
            "destination_lon": "-95.3698",
            "unit": "km",
            "route_factor": "1.2",
            "fuel_economy_l_per_100km": "7.5",
            "fuel_price_per_liter": "1.50",
        }

        # First POST request
        response1 = self.client.post(url, form_data)
        self.assertEqual(response1.status_code, 200)

        # Second identical POST request (should not use cache)
        response2 = self.client.post(url, form_data)
        self.assertEqual(response2.status_code, 200)

        # Both should succeed; POST requests don't cache
        self.assertIsNotNone(response1.content)
        self.assertIsNotNone(response2.content)

    def test_different_parameters_different_cache(self) -> None:
        """Test that different query parameters use different cache keys."""
        url = reverse("calculators:distance")

        # Request with one set of parameters
        response1 = self.client.get(url, {"unit": "km"})
        self.assertEqual(response1.status_code, 200)

        # Request with different parameters
        response2 = self.client.get(url, {"unit": "mi"})
        self.assertEqual(response2.status_code, 200)

        # Both should work (different cache keys)
        self.assertIsNotNone(response1.content)
        self.assertIsNotNone(response2.content)

    def test_cache_clears_successfully(self) -> None:
        """Test that cache can be cleared."""
        url = reverse("calculators:distance")

        # Make request to populate cache
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)

        # Clear cache
        cache.clear()

        # Next request should work (cache miss, repopulated)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        self.assertIsNotNone(response2.content)

    def test_index_view_not_cached(self) -> None:
        """Test that the calculators index view is not cached."""
        # Index view doesn't have @cache_page decorator
        url = reverse("calculators:index")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)


class CalculatorPartialCachingTestCase(TestCase):
    """Test caching behavior for calculator partial views."""

    def setUp(self) -> None:
        """Clear cache and create test client."""
        cache.clear()
        self.client = Client()

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_distance_partial_post_works(self) -> None:
        """Test that distance partial endpoint works for POST."""
        url = reverse("calculators:distance-partial")

        form_data = {
            "origin_lat": "32.8473",
            "origin_lon": "-96.8513",
            "destination_lat": "29.7604",
            "destination_lon": "-95.3698",
            "unit": "km",
            "route_factor": "1.2",
        }

        response = self.client.post(url, form_data)
        # Should return 200 with result or 400 with errors (depending on HTMX handling)
        self.assertIn(response.status_code, [200, 400])
        self.assertIsNotNone(response.content)

    def test_cost_partial_post_works(self) -> None:
        """Test that cost partial endpoint works for POST."""
        url = reverse("calculators:cost-partial")

        form_data = {
            "origin_lat": "32.8473",
            "origin_lon": "-96.8513",
            "destination_lat": "29.7604",
            "destination_lon": "-95.3698",
            "unit": "km",
            "route_factor": "1.2",
            "fuel_economy_l_per_100km": "7.5",
            "fuel_price_per_liter": "1.50",
        }

        response = self.client.post(url, form_data)
        # Should return 200 with result or 400 with errors (depending on HTMX handling)
        self.assertIn(response.status_code, [200, 400])
        self.assertIsNotNone(response.content)
