from django.test import TestCase
from django.urls import reverse


class BaseURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("base:index"), "/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("base:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base/index.html")
        # Global base template lives at travelmathlite/templates/base.html
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Base app partial include.")
