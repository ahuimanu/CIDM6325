"""Template tests for airports app.

Tests template rendering, HTMX partial behavior, and navigation.
"""

from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Airport


class NearestTemplateTests(TestCase):
    """Test nearest airport templates and HTMX partials."""

    @classmethod
    def setUpTestData(cls):
        """Create test airports for template rendering."""
        cls.airport1 = Airport.objects.create(
            ident="KDFW",
            airport_type="large_airport",
            name="Dallas Fort Worth International Airport",
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            municipality="Dallas",
            iso_country="US",
            iata_code="DFW",
        )
        cls.airport2 = Airport.objects.create(
            ident="KDAL",
            airport_type="medium_airport",
            name="Dallas Love Field",
            latitude_deg=32.8471,
            longitude_deg=-96.8518,
            municipality="Dallas",
            iso_country="US",
            iata_code="DAL",
        )

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.url = reverse("airports:nearest")

    def test_get_renders_form(self):
        """GET request should render form with no results."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airports/nearest.html")
        self.assertContains(response, "Nearest Airports")
        self.assertContains(response, "<form")
        self.assertContains(response, "hx-post")
        self.assertContains(response, 'id="results-container"')
        self.assertNotContains(response, "Results (")

    def test_post_renders_full_page_with_results(self):
        """POST request without HTMX should render full page with results."""
        response = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",  # DFW coordinates
                "unit": "mi",
                "limit": 3,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airports/nearest.html")
        self.assertContains(response, "Results (mi)")
        self.assertContains(response, "Dallas Fort Worth International Airport")

    def test_htmx_post_renders_partial_only(self):
        """HTMX POST request should render only the partial template."""
        response = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",  # DFW coordinates
                "unit": "km",
                "limit": 2,
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airports/partials/nearest_results.html")
        self.assertContains(response, "Results (km)")
        self.assertContains(response, "Dallas Fort Worth International Airport")
        # Should not contain full page elements
        self.assertNotContains(response, "<html")
        self.assertNotContains(response, "<form")

    def test_htmx_post_invalid_form_returns_partial(self):
        """HTMX POST with invalid form should return partial with no results."""
        response = self.client.post(
            self.url,
            {
                "query": "",  # Invalid: empty query
                "unit": "km",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airports/partials/nearest_results.html")
        self.assertContains(response, "No results found")

    def test_partial_template_renders_correctly(self):
        """Partial template should render results with proper structure."""
        response = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",  # DFW coordinates
                "unit": "mi",
                "limit": 1,
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Results (mi)</h2>")
        self.assertContains(response, "<ol>")
        self.assertContains(response, "<li>")
        self.assertContains(response, "Dallas Fort Worth International Airport")
        self.assertContains(response, "(DFW)")
        self.assertContains(response, "mi")

    def test_partial_shows_both_units(self):
        """Partial should correctly display distance in km or mi."""
        # Test km
        response_km = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",
                "unit": "km",
                "limit": 1,
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertContains(response_km, "Results (km)")
        self.assertContains(response_km, "km")

        # Test mi
        response_mi = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",
                "unit": "mi",
                "limit": 1,
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertContains(response_mi, "Results (mi)")
        self.assertContains(response_mi, "mi")

    def test_nav_link_present_in_base(self):
        """Base template should have navigation link to nearest airports."""
        response = self.client.get(self.url)
        self.assertContains(response, 'href="/airports/nearest/"')
        self.assertContains(response, "Nearest")

    def test_partial_includes_airport_details(self):
        """Partial should include airport name, code, and location details."""
        response = self.client.post(
            self.url,
            {
                "query": "32.8968,-97.0380",  # DFW coordinates
                "unit": "mi",
                "limit": 2,
            },
            HTTP_HX_REQUEST="true",
        )

        # Check for airport name
        self.assertContains(response, "Dallas Fort Worth International Airport")
        # Check for IATA code
        self.assertContains(response, "(DFW)")
        # Check for municipality
        self.assertContains(response, "Dallas")
        # Check for country code
        self.assertContains(response, "US")

    def test_partial_handles_no_results(self):
        """Partial should show appropriate message when no results found."""
        response = self.client.post(
            self.url,
            {
                "query": "0,0",  # Middle of ocean, likely no airports nearby
                "unit": "km",
                "limit": 1,
                "iso_country": "XX",  # Invalid country
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertContains(response, "No results found")
