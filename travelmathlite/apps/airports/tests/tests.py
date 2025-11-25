from django.test import TestCase
from django.urls import reverse


class AirportsURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("airports:index"), "/airports/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("airports:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "airports/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Airports app partial include.")
