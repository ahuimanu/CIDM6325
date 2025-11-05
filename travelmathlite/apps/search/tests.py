from django.test import TestCase
from django.urls import reverse


class SearchURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("search:index"), "/search/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("search:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "search/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Search app partial include.")
