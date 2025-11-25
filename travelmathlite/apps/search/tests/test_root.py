"""Original search view & highlight tests relocated into tests package.

Avoid name collision between module `tests` and package `tests` by renaming.
"""

from django.test import TestCase
from django.urls import reverse

from ...airports.models import Airport
from ...base.models import City, Country
from ..templatetags.highlight import highlight


class SearchViewTests(TestCase):
    def setUp(self) -> None:  # noqa: D401
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
        )

    def test_search_no_query_returns_empty(self) -> None:
        url = reverse("search:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 0)
        self.assertFalse(resp.context["had_query"])

    def test_search_with_query_returns_results(self) -> None:
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Cached responses may drop context; rely on HTML content instead
        self.assertIn(b"Dallas", resp.content)
        self.assertIn(b"DAL", resp.content)

    def test_pagination_preserves_query_string(self) -> None:
        for i in range(25):
            Airport.objects.create(
                ident=f"TEST{i:02d}",
                iata_code=f"T{i:02d}",
                name=f"Test Airport {i}",
                municipality="TestCity",
                iso_country="US",
                country=self.country,
                city=self.city,
                latitude_deg=32.0 + (i * 0.1),
                longitude_deg=-96.0 + (i * 0.1),
            )
        url = reverse("search:index") + "?q=Test"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["page_obj"].has_next())
        self.assertContains(resp, "?q=Test&page=2")

    def test_canonical_link_in_results(self) -> None:
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<link rel="canonical"')
        self.assertContains(resp, "?q=Dallas")


class HighlightFilterTests(TestCase):
    def test_highlight_wraps_match_in_mark_tags(self) -> None:
        result = highlight("Dallas Love Field", "Love")
        self.assertIn("<mark>Love</mark>", result)

    def test_highlight_escapes_html_in_text(self) -> None:
        result = highlight("<script>alert('xss')</script>", "script")
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)
        self.assertNotIn("<script>", result)

    def test_highlight_escapes_regex_special_chars_in_query(self) -> None:
        result = highlight("Cost is $100", "$100")
        self.assertIn("<mark>$100</mark>", result)

    def test_highlight_case_insensitive(self) -> None:
        result = highlight("Dallas Love Field", "love")
        self.assertIn("<mark>Love</mark>", result)

    def test_highlight_empty_query_returns_original(self) -> None:
        result = highlight("Dallas Love Field", "")
        self.assertEqual(result, "Dallas Love Field")

    def test_highlight_no_match_returns_escaped_text(self) -> None:
        result = highlight("Dallas Love Field", "Houston")
        self.assertEqual(result, "Dallas Love Field")
        self.assertNotIn("<mark>", result)
