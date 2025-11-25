"""View and form tests for calculators app.

Covers Distance and Cost calculator views: GET form rendering, valid and
invalid POST handling, HTMX partial responses, and partial endpoints.

Brief: adr-1.0.11-03-view-tests (Issue #86)
PRD §4 F-011 / FR-F-011-1
Invariants: INV-1 deterministic, INV-2 HTMX/full-page dual behavior.
"""

from __future__ import annotations

from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..forms import CostCalculatorForm, DistanceCalculatorForm
from ..views import (
    DistanceCalculatorView,
)


class CalculatorViewTests(TestCase):
    """Tests for calculator CBVs using RequestFactory and test client."""

    def setUp(self) -> None:  # noqa: D401 (simple setup)
        self.factory = RequestFactory()

        # Common valid data (cities resolved via deterministic mapping)
        self.distance_data = {
            "origin": "London",
            "destination": "Paris",
            "unit": "km",
            "route_factor": 1.2,
        }

        self.cost_data = {
            **self.distance_data,
            "fuel_economy_l_per_100km": 7.5,
            "fuel_price_per_liter": 1.50,
        }

    # -------------------- Index --------------------
    def test_index_get_renders_template(self):
        url = reverse("calculators:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculators/index.html")

    # -------------------- Distance GET --------------------
    def test_distance_get_renders_form(self):
        url = reverse("calculators:distance")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculators/distance_calculator.html")
        self.assertIsInstance(response.context["form"], DistanceCalculatorForm)

    # -------------------- Distance POST valid --------------------
    def test_distance_post_valid_returns_context(self):
        url = reverse("calculators:distance")
        response = self.client.post(url, data=self.distance_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("flight_distance", response.context)
        self.assertIn("driving_distance", response.context)
        self.assertIn("driving_time_hours", response.context)

    # -------------------- Distance POST invalid --------------------
    def test_distance_post_invalid_shows_errors(self):
        url = reverse("calculators:distance")
        bad = {**self.distance_data, "origin": "InvalidCity"}
        response = self.client.post(url, data=bad)
        # FormView default invalid returns 200 with errors
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("origin", form.errors)

    # -------------------- Distance POST HTMX valid --------------------
    def test_distance_post_htmx_returns_partial(self):
        url = reverse("calculators:distance")
        response = self.client.post(url, data=self.distance_data, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        # Partial template content includes human-readable label
        self.assertIn("Estimated driving distance:", response.content.decode())

    # -------------------- Distance POST HTMX invalid --------------------
    def test_distance_post_invalid_htmx_returns_partial_400(self):
        url = reverse("calculators:distance")
        bad = {**self.distance_data, "origin": "BadCity"}
        response = self.client.post(url, data=bad, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 400)
        # Error alert shown with heading
        body = response.content.decode()
        self.assertIn("Please correct the following errors:", body)
        self.assertIn("Unknown city: BadCity", body)

    # -------------------- Distance Partial endpoint invalid --------------------
    def test_distance_partial_invalid_returns_full_page(self):
        # Partial endpoint in views overrides form_invalid to render full page
        url = reverse("calculators:distance-partial")
        bad = {**self.distance_data, "origin": "BadCity"}
        response = self.client.post(url, data=bad)
        self.assertEqual(response.status_code, 400)
        self.assertIn("distance_calculator.html", response.templates[0].name)

    # -------------------- Cost GET --------------------
    def test_cost_get_renders_form(self):
        url = reverse("calculators:cost")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculators/cost_calculator.html")
        self.assertIsInstance(response.context["form"], CostCalculatorForm)

    # -------------------- Cost POST valid --------------------
    def test_cost_post_valid_includes_fuel_cost(self):
        url = reverse("calculators:cost")
        response = self.client.post(url, data=self.cost_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("fuel_cost", response.context)
        self.assertGreaterEqual(response.context["fuel_cost"], 0)

    # -------------------- Cost POST invalid --------------------
    def test_cost_post_invalid_shows_errors(self):
        url = reverse("calculators:cost")
        bad = {**self.cost_data, "origin": "UnknownCity"}
        response = self.client.post(url, data=bad)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("origin", form.errors)

    # -------------------- Cost POST HTMX valid --------------------
    def test_cost_post_htmx_returns_partial(self):
        url = reverse("calculators:cost")
        response = self.client.post(url, data=self.cost_data, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Estimated fuel cost:", response.content.decode())

    # -------------------- Cost POST HTMX invalid --------------------
    def test_cost_post_invalid_htmx_returns_partial_400(self):
        url = reverse("calculators:cost")
        bad = {**self.cost_data, "origin": "UnknownCity"}
        response = self.client.post(url, data=bad, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 400)
        body = response.content.decode()
        self.assertIn("Please correct the following errors:", body)
        self.assertIn("Unknown city: UnknownCity", body)

    # -------------------- Cost Partial endpoint invalid --------------------
    def test_cost_partial_invalid_returns_full_page(self):
        url = reverse("calculators:cost-partial")
        bad = {**self.cost_data, "origin": "UnknownCity"}
        response = self.client.post(url, data=bad)
        self.assertEqual(response.status_code, 400)
        self.assertIn("cost_calculator.html", response.templates[0].name)

    # -------------------- RequestFactory direct invocation sample --------------------
    def test_distance_view_requestfactory_direct(self):
        """Demonstrate RequestFactory: ensures form_valid path works manually."""
        request = self.factory.post(
            reverse("calculators:distance"),
            data=self.distance_data,
            HTTP_HX_REQUEST="true",
        )
        response = DistanceCalculatorView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Estimated driving distance:", response.content.decode())
