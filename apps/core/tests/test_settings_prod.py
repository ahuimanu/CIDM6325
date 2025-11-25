"""Tests for production settings compliance.

These tests validate that the `core.settings.prod` import enforces the
security-related invariants described in ADR-1.0.8.
"""

from importlib import import_module
from unittest.mock import patch
from typing import Any

from django.test import TestCase


class ProdSettingsTest(TestCase):
    """Verify production settings enforce security invariants."""

    @patch(
        "os.environ",
        {
            "SECRET_KEY": "fake-secret-for-tests",
            "ALLOWED_HOSTS": "example.com",
            "USE_WHITENOISE": "1",
        },
    )
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
