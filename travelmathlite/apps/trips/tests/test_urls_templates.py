from django.test import TestCase
from django.urls import reverse


class TripsURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("trips:index"), "/trips/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("trips:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "trips/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Trips app partial include.")
