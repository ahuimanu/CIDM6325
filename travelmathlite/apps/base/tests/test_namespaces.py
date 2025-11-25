from __future__ import annotations

from django.test import TestCase
from django.urls import NoReverseMatch, reverse


class NamespacesExistenceTests(TestCase):
    """Shared sanity checks for app namespaces and index routes.

    This lives in the "base" app's tests package so Django's test discovery
    picks it up without additional settings.
    """

    expected: dict[str, str] = {
        "base": "/",
        "calculators": "/calculators/",
        "airports": "/airports/",
        "accounts": "/accounts/",
        "trips": "/trips/",
        "search": "/search/",
    }

    def test_all_namespaces_reverse(self) -> None:
        for ns, path in self.expected.items():
            with self.subTest(namespace=ns):
                url = reverse(f"{ns}:index")
                self.assertEqual(url, path)

    def test_missing_namespace_raises(self) -> None:
        with self.assertRaises(NoReverseMatch):
            reverse("nonexistent:index")
