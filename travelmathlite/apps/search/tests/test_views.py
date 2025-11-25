"""Search view tests per Brief 04.

Covers SearchView behavior: empty query, basic query matching, pagination,
case sensitivity, and deterministic combined results list.

Issue: #88 (adr-1.0.11-04-search-tests)
PRD §4 F-011 / FR-F-011-1
"""

from __future__ import annotations

from django.test import TestCase, override_settings
from django.urls import reverse

from ...airports.models import Airport
from ...base.models import City, Country


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class SearchViewBehaviorTests(TestCase):
    def setUp(self) -> None:  # noqa: D401
        self.country = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="united-states",
        )
        self.city = City.objects.create(country=self.country, name="Dallas", slug="dallas")
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
        )

    def test_empty_query_context(self) -> None:
        url = reverse("search:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["query"], "")
        self.assertFalse(resp.context["had_query"])
        self.assertEqual(resp.context["results_count"], 0)
        self.assertIsNone(resp.context["page_obj"])

    def test_basic_city_query_returns_results(self) -> None:
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["had_query"])
        self.assertEqual(resp.context["query"], "Dallas")
        self.assertGreaterEqual(resp.context["results_count"], 1)
        # Combined results list contains tuples (type, obj)
        self.assertIsInstance(resp.context["results"], list)
        self.assertIsInstance(resp.context["results"][0], tuple)

    def test_airport_query_returns_airport_first(self) -> None:
        url = reverse("search:index") + "?q=Love"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(resp.context["results_count"], 0)
        first_type, first_obj = resp.context["results"][0]
        # Airports are grouped first by view logic
        self.assertEqual(first_type, "airport")
        self.assertIn("Love", first_obj.name)

    def test_pagination_multiple_pages(self) -> None:
        # Create 30 airports matching 'Test'
        for i in range(30):
            Airport.objects.create(
                ident=f"TEST{i:02d}",
                iata_code=f"T{i:02d}",
                name=f"Test Airport {i}",
                municipality="Dallas",
                iso_country="US",
                country=self.country,
                city=self.city,
                latitude_deg=32.0 + i * 0.01,
                longitude_deg=-96.0 - i * 0.01,
            )
        url = reverse("search:index") + "?q=Test"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        page_obj = resp.context["page_obj"]
        self.assertTrue(page_obj.has_next())
        self.assertEqual(page_obj.number, 1)

        # Page 2
        resp2 = self.client.get(url + "&page=2")
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.context["page_obj"].number, 2)
        self.assertNotEqual(resp.content, resp2.content)

    def test_query_whitespace_trimmed(self) -> None:
        url = reverse("search:index") + "?q=%20Dallas%20%20"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["query"], "Dallas")

    def test_case_sensitive_distinct_queries(self) -> None:
        # View stores original query; search uses icontains so results should match regardless of case
        url_lower = reverse("search:index") + "?q=dallas"
        url_mixed = reverse("search:index") + "?q=Dallas"
        resp1 = self.client.get(url_lower)
        resp2 = self.client.get(url_mixed)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        # Query strings preserved in context
        self.assertEqual(resp1.context["query"], "dallas")
        self.assertEqual(resp2.context["query"], "Dallas")
        # Results count should be > 0 and identical logically
        self.assertGreater(resp1.context["results_count"], 0)
        self.assertEqual(resp1.context["results_count"], resp2.context["results_count"])

    def test_unknown_query_returns_zero_results(self) -> None:
        url = reverse("search:index") + "?q=NonexistentXYZ"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 0)
        self.assertTrue(resp.context["had_query"])

    def test_combined_results_structure(self) -> None:
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        combined = resp.context["results"]
        self.assertIsInstance(combined, list)
        for kind, _obj in combined:
            self.assertIn(kind, {"airport", "city"})
