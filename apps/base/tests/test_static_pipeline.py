from django.test import TestCase, override_settings
from django.templatetags.static import static
from django.conf import settings
from unittest.mock import patch


class StaticPipelineTests(TestCase):
    def test_static_url_without_manifest_returns_unmodified_path(self):
        # When using the default StaticFilesStorage, static() should return
        # the expected path under STATIC_URL.
        settings.STATIC_URL = "/static/"
        path = static("vendor/bootstrap/css/bootstrap.min.css")
        self.assertTrue(path.endswith("/vendor/bootstrap/css/bootstrap.min.css"))

    def test_static_url_with_mocked_manifest_returns_hashed_name(self):
        # Simulate a manifest by patching staticfiles_storage.url to return
        # a hashed filename and verify that templates will see the hashed path.
        hashed = "/static/vendor/bootstrap/css/bootstrap.min.abcdef123.css"

        with patch(
            "django.contrib.staticfiles.storage.staticfiles_storage.url", return_value=hashed
        ):
            path = static("vendor/bootstrap/css/bootstrap.min.css")
            self.assertEqual(path, hashed)
