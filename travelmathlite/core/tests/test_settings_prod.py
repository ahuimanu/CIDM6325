"""Tests for production settings compliance located in the project `core` package.

Placing the test under `core.tests` ensures Django's test runner can discover
and import the module reliably from the project package path.
"""

from importlib import import_module
from typing import Any
from unittest.mock import patch

from django.test import TestCase


class ProdSettingsTest(TestCase):
    """Verify production settings enforce security invariants."""

    @patch("os.environ", {"SECRET_KEY": "fake-secret-for-tests", "ALLOWED_HOSTS": "example.com", "USE_WHITENOISE": "1"})
    def test_prod_settings_requirements_and_flags(self) -> None:
        prod: Any = import_module("core.settings.prod")

        # DEBUG must be False in production
        self.assertFalse(getattr(prod, "DEBUG", True))

        # Security flags should be enabled by default in prod
        self.assertTrue(getattr(prod, "SESSION_COOKIE_SECURE", False))
        self.assertTrue(getattr(prod, "CSRF_COOKIE_SECURE", False))

        # WhiteNoise flag should be present (env-controlled)
        self.assertTrue(getattr(prod, "USE_WHITENOISE", False))

        # ALLOWED_HOSTS should be populated from the env
        self.assertTrue(getattr(prod, "ALLOWED_HOSTS", []))
