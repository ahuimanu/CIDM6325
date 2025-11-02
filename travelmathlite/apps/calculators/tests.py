from django.test import TestCase
from django.urls import reverse


class CalculatorsURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("calculators:index"), "/calculators/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("calculators:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Calculators app partial include.")
