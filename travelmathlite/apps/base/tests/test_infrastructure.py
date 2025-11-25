"""Tests for base test infrastructure.

Demonstrates usage of BaseTestCase, MockingTestCase, and TimeTestCase.
"""

from django.utils import timezone

from .base import BaseTestCase, MockingTestCase, TimeTestCase


class BaseTestCaseTests(BaseTestCase):
    """Test the BaseTestCase infrastructure."""

    def test_create_user(self):
        """Test user creation fixture."""
        user = self.create_user(username="testuser", email="test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test superuser creation fixture."""
        admin = self.create_superuser(username="admin")
        self.assertEqual(admin.username, "admin")
        self.assertTrue(admin.is_superuser)

    def test_make_request(self):
        """Test RequestFactory helper."""
        user = self.create_user()
        request = self.make_request("GET", "/test/", user=user)

        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/test/")
        self.assertEqual(request.user, user)


class MockingTestCaseTests(MockingTestCase):
    """Test the MockingTestCase infrastructure."""

    def test_mock_external_api_with_return_value(self):
        """Test generic API mocking with return value."""
        # Mock Django's timezone.now
        fixed_time = timezone.datetime(2025, 11, 19, 12, 0, 0, tzinfo=timezone.get_current_timezone())
        mock_fn = self.mock_external_api("django.utils.timezone.now", return_value=fixed_time)

        # Verify mock was created
        self.assertIsNotNone(mock_fn)
        # Verify mocks are tracked (the patch object is tracked, not the MagicMock)
        self.assertEqual(len(self._mocks), 1)

        # Verify the mock works
        self.assertEqual(timezone.now(), fixed_time)

    def test_mock_cleanup(self):
        """Test that mocks are tracked for cleanup."""
        # Create mock
        self.mock_external_api("django.utils.timezone.now", return_value=timezone.now())

        # Verify it's tracked
        self.assertEqual(len(self._mocks), 1)


class TimeTestCaseTests(TimeTestCase):
    """Test the TimeTestCase infrastructure."""

    def test_freeze_time(self):
        """Test time freezing."""
        fixed_time = self.get_fixed_datetime(2025, 11, 19, hour=12, minute=0, second=0)
        self.freeze_time(fixed_time)

        # Now timezone.now() should return our fixed time
        current = timezone.now()
        self.assertEqual(current, fixed_time)

    def test_get_fixed_datetime(self):
        """Test fixed datetime generation."""
        dt = self.get_fixed_datetime(2025, 11, 19, hour=15, minute=30, second=45)

        self.assertEqual(dt.year, 2025)
        self.assertEqual(dt.month, 11)
        self.assertEqual(dt.day, 19)
        self.assertEqual(dt.hour, 15)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(dt.second, 45)
        # Should be timezone-aware
        self.assertIsNotNone(dt.tzinfo)
