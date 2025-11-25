"""Tests for request ID and timing middleware.

Tests verify ADR-1.0.9 requirements:
- INV-1: request.request_id is always present
- INV-2: request.duration_ms is logged even on exceptions
"""

import uuid

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from core.middleware import RequestIDMiddleware


class RequestIDMiddlewareTestCase(TestCase):
    """Test RequestIDMiddleware behavior."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.factory = RequestFactory()

        # Create a simple view that returns a successful response
        def simple_view(request):
            return HttpResponse("OK")

        self.middleware = RequestIDMiddleware(simple_view)

    def test_generates_request_id_when_not_provided(self) -> None:
        """Test that middleware generates UUID4 when X-Request-ID is missing."""
        request = self.factory.get("/test/")
        response = self.middleware(request)

        # INV-1: request_id must always be present
        self.assertTrue(hasattr(request, "request_id"))
        self.assertIsNotNone(request.request_id)

        # Should be a valid UUID format
        try:
            uuid_obj = uuid.UUID(request.request_id)
            self.assertEqual(uuid_obj.version, 4)
        except ValueError:
            self.fail("Generated request_id is not a valid UUID4")

        # Response should echo the request ID
        self.assertEqual(response["X-Request-ID"], request.request_id)

    def test_uses_provided_request_id_from_header(self) -> None:
        """Test that middleware uses X-Request-ID from request headers."""
        test_id = "test-request-id-12345"
        request = self.factory.get("/test/", headers={"X-Request-ID": test_id})
        response = self.middleware(request)

        # Should use the provided ID
        self.assertEqual(request.request_id, test_id)

        # Response should echo the same ID
        self.assertEqual(response["X-Request-ID"], test_id)

    def test_calculates_duration_in_milliseconds(self) -> None:
        """Test that middleware calculates request duration in milliseconds."""
        request = self.factory.get("/test/")
        self.middleware(request)

        # duration_ms should be set
        self.assertTrue(hasattr(request, "duration_ms"))
        self.assertIsNotNone(request.duration_ms)

        # Should be a positive number (milliseconds)
        self.assertGreater(request.duration_ms, 0)
        self.assertIsInstance(request.duration_ms, float)

    def test_duration_recorded_on_exception(self) -> None:
        """Test INV-2: duration_ms is logged even when view raises exception."""

        # Create a view that raises an exception
        def failing_view(request):
            raise ValueError("Test exception")

        middleware = RequestIDMiddleware(failing_view)
        request = self.factory.get("/test/")

        # The middleware should let the exception propagate but still set duration
        with self.assertRaises(ValueError):
            middleware(request)

        # INV-2: duration_ms must be set even on exception
        self.assertTrue(hasattr(request, "duration_ms"))
        self.assertIsNotNone(request.duration_ms)
        self.assertGreater(request.duration_ms, 0)

        # INV-1: request_id must also be set
        self.assertTrue(hasattr(request, "request_id"))
        self.assertIsNotNone(request.request_id)

    def test_request_id_persists_through_middleware_chain(self) -> None:
        """Test that request_id is accessible throughout request processing."""
        collected_id = None

        def view_that_reads_id(request):
            nonlocal collected_id
            collected_id = request.request_id
            return HttpResponse("OK")

        middleware = RequestIDMiddleware(view_that_reads_id)
        request = self.factory.get("/test/")
        response = middleware(request)

        # View should have been able to read request_id
        self.assertIsNotNone(collected_id)
        self.assertEqual(collected_id, request.request_id)
        self.assertEqual(response["X-Request-ID"], collected_id)

    def test_different_requests_get_different_ids(self) -> None:
        """Test that each request without X-Request-ID gets a unique ID."""
        request1 = self.factory.get("/test/")
        request2 = self.factory.get("/test/")

        self.middleware(request1)
        self.middleware(request2)

        # Two requests should have different IDs
        self.assertNotEqual(request1.request_id, request2.request_id)
