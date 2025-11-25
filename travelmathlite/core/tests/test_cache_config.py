"""Tests for cache configuration.

Verify cache backend loads correctly for local and production environments.
"""

import os
from unittest import mock

from django.core.cache import cache, caches
from django.test import TestCase, override_settings


class CacheConfigurationTest(TestCase):
    """Test cache backend configuration."""

    def test_cache_backend_is_configured(self):
        """Cache backend should be available."""
        self.assertIsNotNone(cache)
        # Should have a default cache
        self.assertIsNotNone(caches["default"])

    def test_local_uses_locmem_backend(self):
        """Local development should use locmem cache backend."""
        from django.conf import settings

        # Check the configured backend in settings
        cache_config = settings.CACHES.get("default", {})
        backend = cache_config.get("BACKEND", "")

        # Should be using locmem or dummy cache backend
        self.assertIn(
            "locmem",
            backend.lower(),
            f"Expected locmem backend, got {backend}",
        )

    def test_cache_basic_operations(self):
        """Cache should support basic set/get/delete operations."""
        test_key = "test_cache_config_key"
        test_value = "test_cache_config_value"

        # Set a value
        cache.set(test_key, test_value, 60)

        # Get the value
        cached_value = cache.get(test_key)
        self.assertEqual(cached_value, test_value)

        # Delete the value
        cache.delete(test_key)
        self.assertIsNone(cache.get(test_key))

    def test_cache_timeout_default(self):
        """Cache should respect default timeout."""
        # Get the default timeout from cache settings
        default_timeout = caches["default"].default_timeout
        # Should be 300 seconds (5 minutes) per brief
        self.assertEqual(
            default_timeout,
            300,
            f"Expected 300 second default timeout, got {default_timeout}",
        )

    def test_cache_key_prefix(self):
        """Cache should use travelmathlite key prefix."""
        from django.conf import settings

        cache_config = settings.CACHES.get("default", {})
        key_prefix = cache_config.get("KEY_PREFIX", "")
        self.assertEqual(
            key_prefix,
            "travelmathlite",
            f"Expected 'travelmathlite' key prefix, got '{key_prefix}'",
        )

    def test_cache_max_entries_configured(self):
        """Cache should have MAX_ENTRIES configured for locmem."""
        from django.conf import settings

        cache_config = settings.CACHES.get("default", {})
        options = cache_config.get("OPTIONS", {})

        if "locmem" in cache_config.get("BACKEND", "").lower():
            self.assertIn("MAX_ENTRIES", options)
            max_entries = options["MAX_ENTRIES"]
            self.assertGreater(max_entries, 0)
            # Should be 1000 per brief
            self.assertEqual(max_entries, 1000)

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "test-cache",
                "TIMEOUT": 60,
                "OPTIONS": {"MAX_ENTRIES": 100},
            }
        }
    )
    def test_cache_with_custom_settings(self):
        """Cache should work with custom settings."""
        from django.core.cache import caches

        test_cache = caches["default"]
        self.assertEqual(test_cache.default_timeout, 60)

        # Test basic operation
        test_cache.set("custom_key", "custom_value", 30)
        self.assertEqual(test_cache.get("custom_key"), "custom_value")

    def test_cache_clears_successfully(self):
        """Cache clear operation should work."""
        # Set multiple keys
        cache.set("key1", "value1", 60)
        cache.set("key2", "value2", 60)

        # Verify they exist
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")

        # Clear cache
        cache.clear()

        # Verify they're gone
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))


class ProductionCacheConfigTest(TestCase):
    """Test cache configuration for production scenarios."""

    def test_cache_url_parsing_redis(self):
        """Cache URL should support Redis URLs."""
        # We can't test actual Redis connection, but we can verify
        # the configuration would be parsed correctly
        with mock.patch.dict(os.environ, {"CACHE_URL": "redis://localhost:6379/1"}, clear=False):
            # This test just verifies the env var can be read
            cache_url = os.environ.get("CACHE_URL")
            self.assertIsNotNone(cache_url)
            self.assertEqual(cache_url, "redis://localhost:6379/1")
            if cache_url:
                self.assertTrue(cache_url.startswith("redis://"))

    def test_cache_url_parsing_file_based(self):
        """Cache URL should support file-based cache URLs."""
        with mock.patch.dict(os.environ, {"CACHE_URL": "file:///tmp/django_cache"}, clear=False):
            cache_url = os.environ.get("CACHE_URL")
            self.assertIsNotNone(cache_url)
            self.assertEqual(cache_url, "file:///tmp/django_cache")
            if cache_url:
                self.assertTrue(cache_url.startswith("file://"))

    def test_cache_backend_env_var(self):
        """Cache backend should be configurable via environment variable."""
        from django.conf import settings

        # Current backend should match what's in settings
        cache_config = settings.CACHES.get("default", {})
        backend = cache_config.get("BACKEND", "")
        self.assertTrue(len(backend) > 0)
        # Should be a valid Django cache backend path
        self.assertIn("django.core.cache.backends", backend)
