"""Tests for health check endpoint.

Tests verify ADR-1.0.9 health endpoint requirements:
- HTTP 200 response
- JSON payload with status
- X-Commit-SHA header when LOG_COMMIT_SHA is set
"""

import os
from unittest.mock import patch

from django.test import TestCase


class HealthCheckTestCase(TestCase):
    """Test health check endpoint behavior."""

    def test_health_endpoint_returns_200(self) -> None:
        """Test that /health/ returns HTTP 200."""
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_returns_json(self) -> None:
        """Test that /health/ returns JSON content type."""
        response = self.client.get("/health/")
        self.assertEqual(response["Content-Type"], "application/json")

    def test_health_endpoint_returns_ok_status(self) -> None:
        """Test that /health/ returns {"status": "ok"} payload."""
        response = self.client.get("/health/")
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_endpoint_includes_commit_sha_when_configured(self) -> None:
        """Test that X-Commit-SHA header is included when LOG_COMMIT_SHA is set."""
        test_sha = "abc123def456"

        with patch.dict(os.environ, {"LOG_COMMIT_SHA": test_sha}):
            response = self.client.get("/health/")

        self.assertIn("X-Commit-SHA", response)
        self.assertEqual(response["X-Commit-SHA"], test_sha)

    def test_health_endpoint_omits_commit_sha_when_not_configured(self) -> None:
        """Test that X-Commit-SHA header is omitted when LOG_COMMIT_SHA is not set."""
        # Ensure LOG_COMMIT_SHA is not set
        with patch.dict(os.environ, {}, clear=False):
            if "LOG_COMMIT_SHA" in os.environ:
                del os.environ["LOG_COMMIT_SHA"]
            response = self.client.get("/health/")

        self.assertNotIn("X-Commit-SHA", response)

    def test_health_endpoint_with_request_id(self) -> None:
        """Test that health endpoint works with X-Request-ID header from middleware."""
        response = self.client.get("/health/", headers={"X-Request-ID": "test-123"})

        self.assertEqual(response.status_code, 200)
        # Response should echo the request ID (from middleware)
        self.assertIn("X-Request-ID", response)
        self.assertEqual(response["X-Request-ID"], "test-123")

    def test_health_endpoint_accessible_without_auth(self) -> None:
        """Test that /health/ is accessible without authentication."""
        # Anonymous client request
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_handles_head_request(self) -> None:
        """Test that /health/ responds to HEAD requests."""
        response = self.client.head("/health/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_ignores_query_params(self) -> None:
        """Test that health endpoint ignores query parameters."""
        response = self.client.get("/health/?foo=bar&baz=qux")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_endpoint_with_both_headers(self) -> None:
        """Test health endpoint with both X-Request-ID and X-Commit-SHA."""
        test_sha = "abc123"
        test_request_id = "req-456"

        with patch.dict(os.environ, {"LOG_COMMIT_SHA": test_sha}):
            response = self.client.get("/health/", headers={"X-Request-ID": test_request_id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Commit-SHA"], test_sha)
        self.assertEqual(response["X-Request-ID"], test_request_id)
