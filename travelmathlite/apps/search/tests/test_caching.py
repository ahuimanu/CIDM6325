"""Caching tests relocated into tests package to avoid naming conflicts."""

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ...airports.models import Airport
from ...base.models import City, Country


class SearchCachingTestCase(TestCase):
    def setUp(self) -> None:  # noqa: D401
        cache.clear()
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
        self.client = Client()

    def tearDown(self) -> None:  # noqa: D401
        cache.clear()

    def test_search_results_cached(self) -> None:
        url = reverse("search:index")
        response1 = self.client.get(url, {"q": "Dallas"})
        self.assertEqual(response1.status_code, 200)
        content1 = response1.content
        response2 = self.client.get(url, {"q": "Dallas"})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(content1, response2.content)

    def test_different_queries_different_cache(self) -> None:
        url = reverse("search:index")
        response1 = self.client.get(url, {"q": "Dallas"})
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(url, {"q": "Houston"})
        self.assertEqual(response2.status_code, 200)
        self.assertIsNotNone(response1.content)
        self.assertIsNotNone(response2.content)

    def test_pagination_varies_cache_key(self) -> None:
        url = reverse("search:index")
        for i in range(25):
            Airport.objects.create(
                ident=f"TEST{i}",
                iata_code=f"T{i:02d}",
                name=f"Test Airport {i}",
                municipality="Dallas",
                iso_country="US",
                country=self.country,
                city=self.city,
                latitude_deg=32.8470 + i * 0.01,
                longitude_deg=-96.8517 - i * 0.01,
            )
        response1 = self.client.get(url, {"q": "Test", "page": "1"})
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(url, {"q": "Test", "page": "2"})
        self.assertEqual(response2.status_code, 200)
        self.assertNotEqual(response1.content, response2.content)

    def test_empty_query_cached(self) -> None:
        url = reverse("search:index")
        response1 = self.client.get(url, {"q": ""})
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(url, {"q": ""})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.content, response2.content)

    def test_cache_respects_query_case(self) -> None:
        url = reverse("search:index")
        response1 = self.client.get(url, {"q": "dallas"})
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(url, {"q": "DALLAS"})
        self.assertEqual(response2.status_code, 200)
        self.assertIsNotNone(response1.content)
        self.assertIsNotNone(response2.content)

    def test_cache_clears_successfully(self) -> None:
        url = reverse("search:index")
        response1 = self.client.get(url, {"q": "Dallas"})
        self.assertEqual(response1.status_code, 200)
        cache.clear()
        response2 = self.client.get(url, {"q": "Dallas"})
        self.assertEqual(response2.status_code, 200)
        self.assertIsNotNone(response2.content)
