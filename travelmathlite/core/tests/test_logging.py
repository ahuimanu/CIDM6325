"""Tests for structured JSON logging.

Tests verify ADR-1.0.9 logging requirements:
- JSON format with required fields
- Request metadata extraction (request_id, duration_ms)
- Fallback behavior when metadata is missing
"""

import json
import logging
from io import StringIO

from django.test import SimpleTestCase

from core.logging import JSONFormatter


class JSONFormatterTestCase(SimpleTestCase):
    """Test JSONFormatter behavior."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.formatter = JSONFormatter()
        self.logger = logging.getLogger("test_logger")

    def test_formats_basic_log_as_json(self) -> None:
        """Test that formatter outputs valid JSON."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        output = self.formatter.format(record)

        # Should be valid JSON
        parsed = json.loads(output)
        self.assertIsInstance(parsed, dict)

    def test_includes_required_fields(self) -> None:
        """Test that JSON output includes all required fields."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        output = self.formatter.format(record)
        parsed = json.loads(output)

        # Check required fields
        self.assertIn("timestamp", parsed)
        self.assertIn("level", parsed)
        self.assertIn("module", parsed)
        self.assertIn("message", parsed)
        self.assertIn("request_id", parsed)
        self.assertIn("duration_ms", parsed)

    def test_extracts_request_id_from_record(self) -> None:
        """Test that formatter extracts request_id from log record."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.request_id = "test-request-id-12345"  # type: ignore[attr-defined]

        output = self.formatter.format(record)
        parsed = json.loads(output)

        self.assertEqual(parsed["request_id"], "test-request-id-12345")

    def test_extracts_duration_ms_from_record(self) -> None:
        """Test that formatter extracts duration_ms from log record."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.duration_ms = 123.45  # type: ignore[attr-defined]

        output = self.formatter.format(record)
        parsed = json.loads(output)

        self.assertEqual(parsed["duration_ms"], 123.45)

    def test_uses_fallback_when_request_id_missing(self) -> None:
        """Test that formatter uses '-' when request_id is not available."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        output = self.formatter.format(record)
        parsed = json.loads(output)

        self.assertEqual(parsed["request_id"], "-")

    def test_uses_null_when_duration_ms_missing(self) -> None:
        """Test that formatter uses null when duration_ms is not available."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        output = self.formatter.format(record)
        parsed = json.loads(output)

        self.assertIsNone(parsed["duration_ms"])

    def test_formats_different_log_levels(self) -> None:
        """Test that formatter handles different log levels correctly."""
        for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
            with self.subTest(level=level):
                record = logging.LogRecord(
                    name="test_logger",
                    level=level,
                    pathname="test.py",
                    lineno=10,
                    msg="Test message",
                    args=(),
                    exc_info=None,
                )

                output = self.formatter.format(record)
                parsed = json.loads(output)

                self.assertEqual(parsed["level"], logging.getLevelName(level))

    def test_includes_exception_info_when_present(self) -> None:
        """Test that formatter includes exception information."""
        try:
            raise ValueError("Test exception")
        except ValueError:
            import sys

            exc_info = sys.exc_info()

            record = logging.LogRecord(
                name="test_logger",
                level=logging.ERROR,
                pathname="test.py",
                lineno=10,
                msg="Error occurred",
                args=(),
                exc_info=exc_info,
            )

            output = self.formatter.format(record)
            parsed = json.loads(output)

            self.assertIn("exc_info", parsed)
            self.assertIn("ValueError: Test exception", parsed["exc_info"])

    def test_handler_integration(self) -> None:
        """Test that formatter works with a logging handler."""
        # Create a string stream to capture log output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger("integration_test")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent output to root logger

        # Log a message
        logger.info("Integration test message")

        # Get the output
        output = stream.getvalue()
        parsed = json.loads(output.strip())

        self.assertEqual(parsed["message"], "Integration test message")
        self.assertEqual(parsed["level"], "INFO")
        self.assertEqual(parsed["request_id"], "-")

        # Clean up
        logger.removeHandler(handler)

    def test_formats_message_with_args(self) -> None:
        """Test that formatter properly formats messages with arguments."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="User %s logged in from %s",
            args=("john_doe", "192.168.1.1"),
            exc_info=None,
        )

        output = self.formatter.format(record)
        parsed = json.loads(output)

        self.assertEqual(parsed["message"], "User john_doe logged in from 192.168.1.1")
