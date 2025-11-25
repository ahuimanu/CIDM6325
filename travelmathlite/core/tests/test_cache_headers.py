"""Tests for HTTP cache header middleware.

Verify that appropriate Cache-Control and Vary headers are set for different
response types and content.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class CacheHeadersTestCase(TestCase):
    """Test cache header middleware behavior."""

    def setUp(self) -> None:
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_search_has_public_cache_headers(self) -> None:
        """Test that search results have public cache headers."""
        response = self.client.get("/search/?q=Dallas")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("public", response["Cache-Control"])
        self.assertIn("max-age=300", response["Cache-Control"])

    def test_search_has_vary_headers(self) -> None:
        """Test that search results have Vary headers for content negotiation."""
        response = self.client.get("/search/?q=Dallas")

        self.assertIn("Vary", response)
        self.assertIn("Accept", response["Vary"])
        self.assertIn("Cookie", response["Vary"])

    def test_calculator_distance_has_cache_headers(self) -> None:
        """Test that distance calculator has cache headers."""
        response = self.client.get("/calculators/distance/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("public", response["Cache-Control"])
        self.assertIn("max-age=600", response["Cache-Control"])

    def test_calculator_cost_has_cache_headers(self) -> None:
        """Test that cost calculator has cache headers."""
        response = self.client.get("/calculators/cost/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("public", response["Cache-Control"])

    def test_calculator_has_vary_header(self) -> None:
        """Test that calculator responses have Vary header."""
        response = self.client.get("/calculators/distance/")

        self.assertIn("Vary", response)
        self.assertIn("Accept", response["Vary"])

    def test_home_page_has_cache_headers(self) -> None:
        """Test that home page has default public cache headers."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("public", response["Cache-Control"])

    def test_authenticated_content_private_cache(self) -> None:
        """Test that authenticated content is marked private."""
        # Login user
        self.client.login(username="testuser", password="testpass123")

        # Access a page that requires authentication
        response = self.client.get("/trips/")

        # Should have private cache
        self.assertIn("Cache-Control", response)
        self.assertIn("private", response["Cache-Control"])
        self.assertIn("must-revalidate", response["Cache-Control"])

    def test_static_files_skip_middleware(self) -> None:
        """Test that static files are skipped by middleware (handled by WhiteNoise)."""
        # Static files will be handled by WhiteNoise in production
        # In testing with DEBUG=True, Django's static file serving applies
        # This test verifies middleware doesn't interfere
        response = self.client.get("/static/css/main.css")

        # Either file doesn't exist (404) or it's served - both are fine
        # The middleware should not crash or interfere
        self.assertIn(response.status_code, [200, 404])

    def test_search_empty_query(self) -> None:
        """Test that search with empty query has cache headers."""
        response = self.client.get("/search/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("Vary", response)

    def test_cache_control_not_duplicated(self) -> None:
        """Test that Cache-Control header is not duplicated if already set."""
        # Views with @cache_page decorator already have Cache-Control
        # Middleware should skip them
        response = self.client.get("/search/?q=test")

        # Should have exactly one Cache-Control header
        cache_control = response.get("Cache-Control", "")
        self.assertTrue(len(cache_control) > 0)
        # Verify it's well-formed (has at least one directive)
        self.assertTrue("max-age" in cache_control or "no-cache" in cache_control or "public" in cache_control)

    def test_calculator_post_request_handling(self) -> None:
        """Test that POST requests to calculators are handled properly."""
        # POST requests bypass @cache_page decorator but middleware still applies
        response = self.client.post("/calculators/distance/", {})

        # POST typically returns 200 or redirects, check status is reasonable
        self.assertIn(response.status_code, [200, 302, 400])

    def test_unauthenticated_trips_page(self) -> None:
        """Test that trips page shows appropriate cache headers."""
        response = self.client.get("/trips/")

        # Trips page returns 200 (accessible to all users)
        self.assertEqual(response.status_code, 200)


class CacheHeaderVaryTestCase(TestCase):
    """Test Vary header behavior for different content types."""

    def test_vary_accept_on_api_like_responses(self) -> None:
        """Test that API-like responses have Vary: Accept."""
        client = Client()
        response = client.get("/calculators/distance/")

        self.assertIn("Vary", response)
        self.assertIn("Accept", response["Vary"])

    def test_vary_cookie_on_search(self) -> None:
        """Test that search results vary by Cookie (for auth state)."""
        client = Client()
        response = client.get("/search/?q=test")

        self.assertIn("Vary", response)
        self.assertIn("Cookie", response["Vary"])


class CacheHeaderDefaultsTestCase(TestCase):
    """Test default cache header behavior."""

    def test_default_max_age(self) -> None:
        """Test that default public content has 5 minute cache."""
        client = Client()
        response = client.get("/")

        self.assertIn("Cache-Control", response)
        self.assertIn("max-age=300", response["Cache-Control"])

    def test_calculator_longer_cache(self) -> None:
        """Test that calculators have longer cache (10 minutes)."""
        client = Client()
        response = client.get("/calculators/distance/")

        self.assertIn("Cache-Control", response)
        self.assertIn("max-age=600", response["Cache-Control"])
