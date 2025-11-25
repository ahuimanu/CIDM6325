"""Base test classes and utilities for TravelMathLite testing.

This module provides reusable TestCase classes, fixtures, and helper methods
for deterministic, isolated testing across all apps.

Follows ADR-1.0.11 testing strategy: Django TestCase only, no pytest.
"""

from typing import Any
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.utils import timezone


class BaseTestCase(TestCase):
    """Base TestCase with common setup and helper methods.

    Provides:
    - Request factory for view testing
    - User creation fixtures
    - Common assertion helpers
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class-level test data."""
        super().setUpClass()
        cls.factory = RequestFactory()

    def setUp(self) -> None:
        """Set up test fixtures for each test method."""
        super().setUp()
        # Reset any mock state
        self._mocks: list[Any] = []

    def tearDown(self) -> None:
        """Clean up after each test."""
        # Stop any active mocks
        for mock in self._mocks:
            if hasattr(mock, "stop"):
                mock.stop()
        super().tearDown()

    def create_user(
        self,
        username: str = "testuser",
        email: str = "test@example.com",
        password: str = "testpass123",
        **kwargs: Any,
    ) -> Any:
        """Create a test user deterministically.

        Args:
            username: Username for the test user
            email: Email for the test user
            password: Password for the test user
            **kwargs: Additional user model fields

        Returns:
            User instance
        """
        User = get_user_model()
        return User.objects.create_user(username=username, email=email, password=password, **kwargs)

    def create_superuser(
        self,
        username: str = "admin",
        email: str = "admin@example.com",
        password: str = "adminpass123",
        **kwargs: Any,
    ) -> Any:
        """Create a test superuser deterministically.

        Args:
            username: Username for the test superuser
            email: Email for the test superuser
            password: Password for the test superuser
            **kwargs: Additional user model fields

        Returns:
            User instance with superuser privileges
        """
        User = get_user_model()
        return User.objects.create_superuser(username=username, email=email, password=password, **kwargs)

    def make_request(self, method: str = "GET", path: str = "/", user: Any = None, **kwargs: Any) -> Any:
        """Create a request using RequestFactory.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path
            user: User to attach to request (optional)
            **kwargs: Additional request parameters (data, headers, etc.)

        Returns:
            Request object suitable for view testing
        """
        factory_method = getattr(self.factory, method.lower())
        request = factory_method(path, **kwargs)
        if user:
            request.user = user
        return request


class MockingTestCase(BaseTestCase):
    """TestCase with helpers for mocking external calls.

    Provides utilities for mocking HTTP requests, external APIs,
    and other I/O operations to ensure deterministic tests.
    """

    def mock_http_get(self, url: str, response_data: Any, status_code: int = 200) -> Mock:
        """Mock an HTTP GET request.

        Args:
            url: URL to mock
            response_data: Data to return (will be JSON-encoded if dict)
            status_code: HTTP status code to return

        Returns:
            Mock object for further customization
        """
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_response.text = str(response_data)

        mock_get = patch("requests.get", return_value=mock_response)
        mock_obj = mock_get.start()
        self._mocks.append(mock_get)
        return mock_obj

    def mock_http_post(self, url: str, response_data: Any, status_code: int = 200) -> Mock:
        """Mock an HTTP POST request.

        Args:
            url: URL to mock
            response_data: Data to return (will be JSON-encoded if dict)
            status_code: HTTP status code to return

        Returns:
            Mock object for further customization
        """
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_response.text = str(response_data)

        mock_post = patch("requests.post", return_value=mock_response)
        mock_obj = mock_post.start()
        self._mocks.append(mock_post)
        return mock_obj

    def mock_external_api(self, target: str, return_value: Any = None, side_effect: Any = None) -> Mock:
        """Mock an external API call or function.

        Args:
            target: Full import path to patch (e.g., 'apps.calculators.utils.fetch_data')
            return_value: Value to return when called
            side_effect: Side effect (exception, callable, or iterable)

        Returns:
            Mock object for further customization
        """
        mock_patch = patch(target, return_value=return_value, side_effect=side_effect)
        mock_obj = mock_patch.start()
        self._mocks.append(mock_patch)
        return mock_obj


class TimeTestCase(BaseTestCase):
    """TestCase with helpers for time-sensitive testing.

    Provides utilities for freezing time and testing time-dependent logic.
    """

    def freeze_time(self, frozen_time: Any) -> Mock:
        """Freeze time to a specific datetime for deterministic testing.

        Args:
            frozen_time: datetime object or string to freeze time at

        Returns:
            Mock object that can be stopped manually if needed

        Example:
            frozen = self.freeze_time(timezone.datetime(2025, 11, 19, 12, 0, 0))
            # Time is now frozen at noon on Nov 19, 2025
        """
        mock_now = patch("django.utils.timezone.now", return_value=frozen_time)
        mock_obj = mock_now.start()
        self._mocks.append(mock_now)
        return mock_obj

    def get_fixed_datetime(self, year: int = 2025, month: int = 11, day: int = 19, **kwargs: Any) -> Any:
        """Get a timezone-aware datetime for testing.

        Args:
            year: Year
            month: Month
            day: Day
            **kwargs: Additional datetime arguments (hour, minute, second, etc.)

        Returns:
            Timezone-aware datetime object
        """
        dt = timezone.datetime(year, month, day, **kwargs)
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt


# Convenience exports
__all__ = [
    "BaseTestCase",
    "MockingTestCase",
    "TimeTestCase",
]
