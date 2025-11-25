"""Tests for local settings behavior."""

from importlib import import_module
from typing import Any
from unittest.mock import patch

from django.test import TestCase


class LocalSettingsTest(TestCase):
    """Verify local settings default to DEBUG=True and sqlite DB."""

    @patch("os.environ", {})
    def test_local_settings_debug_and_db(self) -> None:
        local: Any = import_module("core.settings.local")

        # Local should enable DEBUG for development convenience
        self.assertTrue(getattr(local, "DEBUG", False))

        # Local DB should be sqlite by default and point to db.sqlite3
        db = getattr(local, "DATABASES", {}).get("default", {})
        engine = db.get("ENGINE")
        name = db.get("NAME")
        self.assertIn("sqlite3", engine)
        # Accept Path or string representation; test runner may use in-memory DB.
        name_str = str(name)
        self.assertTrue(
            ("db.sqlite3" in name_str) or ("memory" in name_str) or (name_str == ""),
            msg=f"Unexpected sqlite NAME: {name_str}",
        )
