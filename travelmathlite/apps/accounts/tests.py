from django.test import TestCase
from django.urls import reverse


class AccountsURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("accounts:index"), "/accounts/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("accounts:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Accounts app partial include.")
