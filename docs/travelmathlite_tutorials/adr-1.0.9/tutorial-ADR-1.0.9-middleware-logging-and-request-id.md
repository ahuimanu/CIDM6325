# Tutorial: Middleware, logging, and request ID (ADR-1.0.9)

Goal

- Teach how to implement observability features for a Django application: custom middleware for request tracing, structured JSON logging with request metadata, and a health check endpoint. This tutorial follows the briefs in `docs/travelmathlite/briefs/adr-1.0.9/`.

Prerequisites

- Python 3.13, virtualenv; repo checked out at project root.
- Project tooling: `uv` helper available (recommended). Activate the project's virtualenv before running commands:

```bash
source .venv/Scripts/activate  # Windows bash-style, adjust if needed
```

- Familiarity with Django basics (middleware, logging, views).
- Existing Django project structure with settings split into `base.py`, `local.py`, `prod.py` (from ADR-1.0.8).

**Repository state note:** This tutorial assumes you are on branch `FALL2025` with the ADR-1.0.9 briefs present. The work completed for this ADR includes:

- `travelmathlite/core/middleware.py` — Request ID and timing middleware
- `travelmathlite/core/logging.py` — JSON formatter for structured logs
- `travelmathlite/core/settings/base.py` — Logging configuration
- `travelmathlite/core/views.py` — Health check endpoint
- `travelmathlite/core/urls.py` — Health endpoint routing
- `travelmathlite/core/tests/test_middleware.py` — Middleware tests
- `travelmathlite/core/tests/test_logging.py` — Logging formatter tests
- `travelmathlite/core/tests/test_health.py` — Health endpoint tests
- `docs/travelmathlite/ops/logging-and-health.md` — Operations documentation

If any of those files are missing, refer to the briefs in `docs/travelmathlite/briefs/adr-1.0.9/` for step-by-step implementation notes.

Overview (Sections)

- Request ID and timing middleware (brief-01)
- Structured JSON logging (brief-02)
- Health check endpoint (brief-03)
- Documentation and testing (brief-04)

---

## Section 1 — Request ID and timing middleware

### Brief context and goal

Implement middleware that injects a unique request identifier (`X-Request-ID`) into every HTTP request and tracks request duration. This enables request tracing across logs and provides timing metrics for performance monitoring.

**Brief:** `docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-01-request-id-middleware.md`

### Relevant Django concepts

#### Django Middleware

From Django documentation:

> Middleware is a framework of hooks into Django's request/response processing. It's a light, low-level "plugin" system for globally altering Django's input or output.

Middleware components are applied in the order they appear in `MIDDLEWARE` setting. Each middleware can:

- Process the request before the view is called
- Process the response after the view returns
- Handle exceptions raised by views

Modern Django middleware uses a callable class with `__init__` and `__call__` methods:

```python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

#### Adding attributes to the request object

Django's `HttpRequest` object can be dynamically extended with custom attributes. This is a common pattern for middleware to attach data that other components (views, loggers) can access:

```python
request.custom_attribute = "value"
```

Type checkers may complain about unknown attributes, but this is standard Django practice. Use `# type: ignore[attr-defined]` to silence type checker warnings.

#### Exception handling in middleware

The `try/finally` pattern in middleware ensures code runs even if the view raises an exception:

```python
def __call__(self, request):
    # Setup code
    try:
        response = self.get_response(request)
    finally:
        # This runs even if view raises exception
        cleanup_code()
    return response
```

### Implementation steps

#### Step 1: Create the middleware module

Create `travelmathlite/core/middleware.py`:

```python
"""Middleware for request ID tracking and timing.

Implements request ID injection and duration tracking as specified in ADR-1.0.9.
Ensures every request has a unique identifier and timing information for logging.
"""

import time
import uuid
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


class RequestIDMiddleware:
    """Inject X-Request-ID and track request duration.
    
    This middleware:
    - Reads X-Request-ID from request headers or generates a UUID4
    - Attaches request_id to the request object for logging
    - Records start/end timestamps and calculates duration_ms
    - Adds X-Request-ID to the response headers
    - Survives exceptions to ensure duration is always available
    
    Invariants:
    - INV-1: request.request_id is always present (never None)
    - INV-2: request.duration_ms is logged even when exceptions occur
    """
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with the next handler in the chain.
        
        Args:
            get_response: The next middleware or view to call.
        """
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process request, inject request ID, and track duration.
        
        Args:
            request: The incoming HTTP request.
            
        Returns:
            The HTTP response with X-Request-ID header added.
        """
        # Read X-Request-ID from headers or generate a new UUID4
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Attach request_id to request for logging (INV-1)
        request.request_id = request_id  # type: ignore[attr-defined]
        
        # Record start time
        start_time = time.perf_counter()
        
        try:
            # Process the request through the rest of the middleware chain
            response = self.get_response(request)
        finally:
            # Calculate duration even if an exception occurred (INV-2)
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000.0
            request.duration_ms = duration_ms  # type: ignore[attr-defined]
        
        # Add X-Request-ID to response headers
        response["X-Request-ID"] = request_id
        
        return response
```

**Key implementation details:**

1. **UUID generation**: Uses `uuid.uuid4()` for globally unique identifiers when no request ID is provided
2. **High-precision timing**: `time.perf_counter()` provides nanosecond precision for accurate duration measurement
3. **Exception safety**: The `try/finally` ensures duration is calculated even if the view raises an exception (satisfies INV-2)
4. **Type annotations**: Uses `collections.abc.Callable` (preferred over `typing.Callable` in Python 3.13+)
5. **Type ignore comments**: Silences linter warnings about dynamic attributes on `HttpRequest`

#### Step 2: Enable the middleware in settings

Update `travelmathlite/core/settings/base.py` to add the middleware early in the stack:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Request ID and timing middleware - must be early for logging
    "core.middleware.RequestIDMiddleware",
    # WhiteNoise placed here so deployments that enable it get static serving
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

**Middleware ordering rationale:**

- Placed after `SecurityMiddleware` (security checks should happen first)
- Placed before other middleware so request ID is available to all downstream components
- Placed before `WhiteNoise` to ensure static file requests are also tracked

### Testing the middleware

#### Step 3: Create comprehensive tests

Create `travelmathlite/core/tests/test_middleware.py`:

```python
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
```

**Testing strategy:**

- Uses Django's `RequestFactory` to create test requests without hitting the network
- Tests both the "happy path" (normal requests) and error cases (exception handling)
- Validates invariants INV-1 and INV-2 explicitly
- Tests UUID format validation using Python's `uuid.UUID` parser
- Uses `nonlocal` to capture values from inner function scopes

#### Step 4: Run the tests

```bash
cd travelmathlite
uv run python manage.py test core.tests.test_middleware
```

**Expected output:**

```
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
Destroying test database for alias 'default'...
```

### Verification

**Manual testing with curl:**

Start the development server:

```bash
cd travelmathlite
uv run python manage.py runserver
```

Test without providing a request ID (server will generate one):

```bash
curl -v http://localhost:8000/
```

Look for the response header:

```
< X-Request-ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Test with your own request ID:

```bash
curl -H "X-Request-ID: my-trace-123" -v http://localhost:8000/
```

The response should echo your ID:

```
< X-Request-ID: my-trace-123
```

---

## Section 2 — Structured JSON logging

### Brief context and goal

Configure Django's logging system to output structured JSON logs that include request metadata (request ID and duration). This enables machine-readable logs that can be easily parsed, searched, and analyzed by log aggregation tools.

**Brief:** `docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-02-structured-logging.md`

### Relevant Python/Django concepts

#### Python logging framework

Python's built-in `logging` module provides a flexible framework for emitting log messages. Key components:

- **Logger**: Entry point for application code (e.g., `logging.getLogger(__name__)`)
- **Handler**: Sends log records to a destination (e.g., console, file)
- **Formatter**: Controls the format of log output
- **Filter**: Provides fine-grained control over which records are processed

Django extends Python's logging with a `LOGGING` setting using `dictConfig` format.

#### Custom log formatters

You can create custom formatters by subclassing `logging.Formatter` and overriding the `format()` method:

```python
import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        # record.levelname, record.getMessage(), record.module, etc.
        return custom_format_string
```

Log records have many attributes you can access:

- `record.levelname` - Log level (INFO, WARNING, ERROR, etc.)
- `record.module` - Module where log originated
- `record.getMessage()` - Formatted message
- Custom attributes can be added: `record.custom_attr = value`

#### JSON serialization

Python's `json` module provides `json.dumps()` to serialize Python objects to JSON strings. This is perfect for structured logging:

```python
import json
log_entry = {"level": "INFO", "message": "User logged in"}
json_line = json.dumps(log_entry)  # One line of JSON
```

### Implementation steps

#### Step 1: Create the JSON formatter

Create `travelmathlite/core/logging.py`:

```python
"""Custom logging formatters for structured logging.

Implements JSON formatter as specified in ADR-1.0.9 for observability.
"""

import json
import logging
from datetime import UTC, datetime


class JSONFormatter(logging.Formatter):
    """Format log records as JSON lines with request metadata.
    
    Emits JSON with fields:
    - timestamp: ISO 8601 format with timezone
    - level: Log level name (INFO, WARNING, ERROR, etc.)
    - module: Module name where log originated
    - message: Formatted log message
    - request_id: Request ID from middleware (or '-' if not available)
    - duration_ms: Request duration from middleware (or null if not available)
    
    The formatter attempts to extract request_id and duration_ms from the
    log record, which are set by RequestIDMiddleware on the request object.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON line.
        
        Args:
            record: The log record to format.
            
        Returns:
            JSON string representing the log entry.
        """
        # Extract request_id from record (set by middleware or custom logging)
        request_id = getattr(record, "request_id", None) or "-"
        
        # Extract duration_ms from record (set by middleware)
        duration_ms = getattr(record, "duration_ms", None)
        
        # Build the log entry
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "request_id": request_id,
            "duration_ms": duration_ms,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)
```

**Key implementation details:**

1. **ISO 8601 timestamps**: Uses `datetime.now(UTC).isoformat()` for timezone-aware, sortable timestamps
2. **Fallback values**: `request_id` defaults to `"-"`, `duration_ms` to `null` when not in request context
3. **Exception handling**: Includes full traceback in `exc_info` field when exceptions are logged
4. **One line per log**: `json.dumps()` produces single-line JSON for easy parsing with tools like `jq`
5. **Attribute extraction**: Uses `getattr()` with defaults to safely access optional attributes

#### Step 2: Configure Django logging

Update `travelmathlite/core/settings/base.py` to add the logging configuration:

```python
# Logging configuration
# Structured JSON logging with request metadata per ADR-1.0.9
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "core.logging.JSONFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

**Configuration explanation:**

- **Formatters**: Registers our custom `JSONFormatter` with the key `"json"`
- **Handlers**: `StreamHandler` outputs to stdout using our JSON formatter
- **Root logger**: Default log level is INFO (configurable via `LOG_LEVEL` env var)
- **Named loggers**: Specialized loggers for Django framework components
  - `django`: General Django logs
  - `django.request`: Request/response logs (WARNING level to reduce noise)
  - `django.server`: Development server logs
- **propagate=False**: Prevents double-logging when child loggers match

#### Step 3: Environment variable configuration

The logging configuration supports these environment variables:

- `LOG_LEVEL`: Root logger level (default: INFO)
- `DJANGO_LOG_LEVEL`: Django framework logger level (default: INFO)

Example usage:

```bash
# Increase verbosity for debugging
export LOG_LEVEL=DEBUG
export DJANGO_LOG_LEVEL=DEBUG

# Reduce noise in production
export LOG_LEVEL=WARNING
export DJANGO_LOG_LEVEL=WARNING
```

### Testing the logging formatter

#### Step 4: Create comprehensive tests

Create `travelmathlite/core/tests/test_logging.py`:

```python
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
```

**Testing strategy:**

- Uses `SimpleTestCase` (no database needed for formatter tests)
- Creates `logging.LogRecord` objects directly for unit testing
- Tests JSON validity with `json.loads()`
- Uses `subTest` for parameterized testing across log levels
- Tests integration with actual `logging.Handler` and `StringIO`
- Uses `logger.propagate = False` to prevent test output pollution

#### Step 5: Run the tests

```bash
cd travelmathlite
uv run python manage.py test core.tests.test_logging
```

**Expected output:**

```
Found 10 test(s).
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

### Verification

**View logs during development:**

Start the server and pipe logs to a file:

```bash
cd travelmathlite
uv run python manage.py runserver 2>&1 | tee logs.json
```

In another terminal, make some requests:

```bash
curl http://localhost:8000/
```

View the JSON logs with pretty-printing:

```bash
tail -10 logs.json | jq .
```

**Example log output:**

```json
{
  "timestamp": "2025-11-19T19:30:45.123456+00:00",
  "level": "INFO",
  "module": "basehttp",
  "message": "GET / HTTP/1.1 200",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "duration_ms": 12.34
}
```

**Filter logs by level:**

```bash
tail -f logs.json | jq 'select(.level == "ERROR")'
```

**Find slow requests:**

```bash
tail -f logs.json | jq 'select(.duration_ms > 100)'
```

---

## Section 3 — Health check endpoint

### Brief context and goal

Implement a simple health check endpoint (`/health/`) that returns HTTP 200 with a JSON status message. This endpoint is used by monitoring systems, load balancers, and orchestration platforms to verify the application is running.

**Brief:** `docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-03-health-endpoint.md`

### Relevant Django concepts

#### Function-based views (FBV)

Django views can be simple functions that take an `HttpRequest` and return an `HttpResponse`:

```python
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello, world!")
```

For JSON responses, use `JsonResponse`:

```python
from django.http import JsonResponse

def json_view(request):
    return JsonResponse({"status": "ok"})
```

`JsonResponse` automatically:

- Sets `Content-Type: application/json`
- Serializes Python dictionaries to JSON
- Returns HTTP 200 by default

#### Adding custom response headers

Django response objects support dictionary-style header assignment:

```python
response = JsonResponse({"status": "ok"})
response["X-Custom-Header"] = "value"
return response
```

#### Environment variables in Django

Access environment variables with Python's `os.getenv()`:

```python
import os

value = os.getenv("ENV_VAR_NAME")  # Returns None if not set
value = os.getenv("ENV_VAR_NAME", "default")  # With default
```

For Django settings managed by `django-environ`, use the `env()` helper (already configured in `base.py`).

### Implementation steps

#### Step 1: Create the health check view

Create `travelmathlite/core/views.py`:

```python
"""Core application views.

Implements health check and operational endpoints per ADR-1.0.9.
"""

import os

from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for monitoring and load balancers.
    
    Returns HTTP 200 with JSON status. Optionally includes X-Commit-SHA
    header when LOG_COMMIT_SHA environment variable is set.
    
    This endpoint is designed to remain accessible even if middleware
    encounters issues, providing a basic liveness check.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        JsonResponse with {"status": "ok"} and HTTP 200.
    """
    response = JsonResponse({"status": "ok"})
    
    # Add commit SHA header if configured
    commit_sha = os.getenv("LOG_COMMIT_SHA")
    if commit_sha:
        response["X-Commit-SHA"] = commit_sha
    
    return response
```

**Key implementation details:**

1. **Simple response**: Just `{"status": "ok"}` - no database queries or complex logic
2. **Optional commit SHA**: Useful for deployment tracking and debugging
3. **Always succeeds**: Returns 200 unless the entire application is down
4. **No authentication required**: Public endpoint for monitoring systems

#### Step 2: Add the URL route

Update `travelmathlite/core/urls.py`:

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import StaticViewSitemap
from .views import health_check

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    # Health check endpoint
    path("health/", health_check, name="health"),
    # Namespaced app URLs
    path("", include("apps.base.urls", namespace="base")),
    # ... rest of URL patterns
]
```

**URL pattern placement:**

- Placed early in `urlpatterns` for visibility
- Uses simple string path (no regex needed)
- Given a name (`"health"`) for reverse URL lookups

### Testing the health endpoint

#### Step 3: Create comprehensive tests

Create `travelmathlite/core/tests/test_health.py`:

```python
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
            response = self.client.get(
                "/health/",
                headers={"X-Request-ID": test_request_id}
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Commit-SHA"], test_sha)
        self.assertEqual(response["X-Request-ID"], test_request_id)
```

**Testing strategy:**

- Uses Django's test `Client` for integration testing
- Tests HTTP methods (GET and HEAD)
- Uses `unittest.mock.patch.dict` to temporarily set environment variables
- Tests interaction with middleware (request ID passthrough)
- Tests both presence and absence of optional features

#### Step 4: Run the tests

```bash
cd travelmathlite
uv run python manage.py test core.tests.test_health
```

**Expected output:**

```
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.049s

OK
Destroying test database for alias 'default'...
```

### Verification

**Test with curl:**

```bash
curl -v http://localhost:8000/health/
```

**Expected response:**

```
HTTP/1.1 200 OK
Content-Type: application/json
X-Request-ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

{"status":"ok"}
```

**Test with commit SHA:**

```bash
export LOG_COMMIT_SHA=$(git rev-parse HEAD)
# Restart server
curl -v http://localhost:8000/health/
```

**Expected response with commit SHA:**

```
HTTP/1.1 200 OK
Content-Type: application/json
X-Request-ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
X-Commit-SHA: abc123def456...

{"status":"ok"}
```

**Test HEAD request:**

```bash
curl -I http://localhost:8000/health/
```

---

## Section 4 — Documentation and testing

### Brief context and goal

Create comprehensive operations documentation covering all three features (middleware, logging, health endpoint) with usage examples, verification commands, and troubleshooting guidance.

**Brief:** `docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-04-docs-and-tests.md`

### Implementation steps

#### Step 1: Create operations documentation

The complete operations guide is at: `docs/travelmathlite/ops/logging-and-health.md`

This comprehensive document includes:

1. **Overview** of all three features
2. **Request ID Middleware** section:
   - Purpose and behavior
   - Configuration details
   - Usage examples
   - Invariants (INV-1, INV-2)
3. **Structured JSON Logging** section:
   - Log format specification
   - Field descriptions
   - Configuration
   - Environment variables
   - Log analysis examples with `jq`
   - Invariant (INV-3)
4. **Health Endpoint** section:
   - Endpoint details
   - Response format
   - Usage examples
   - Configuration for commit SHA
   - Integration examples (Kubernetes, Docker, load balancers)
5. **Testing** section:
   - Test commands
   - Test coverage breakdown
   - Expected outputs
   - CI/CD integration
6. **Additional sections**:
   - Troubleshooting guide
   - Performance considerations
   - Security considerations
   - Maintenance guidelines
   - Quick command reference

#### Step 2: Run all tests together

Verify the complete implementation by running all tests:

```bash
cd travelmathlite
uv run python manage.py test core.tests.test_middleware core.tests.test_logging core.tests.test_health --verbosity=2
```

**Expected output:**

```
Found 26 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

test_calculates_duration_in_milliseconds (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok
test_different_requests_get_different_ids (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok
test_duration_recorded_on_exception (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok
test_generates_request_id_when_not_provided (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok
test_request_id_persists_through_middleware_chain (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok
test_uses_provided_request_id_from_header (core.tests.test_middleware.RequestIDMiddlewareTestCase) ... ok

test_extracts_duration_ms_from_record (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_extracts_request_id_from_record (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_formats_basic_log_as_json (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_formats_different_log_levels (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_formats_message_with_args (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_handler_integration (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_includes_exception_info_when_present (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_includes_required_fields (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_uses_fallback_when_request_id_missing (core.tests.test_logging.JSONFormatterTestCase) ... ok
test_uses_null_when_duration_ms_missing (core.tests.test_logging.JSONFormatterTestCase) ... ok

test_health_endpoint_accessible_without_auth (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_handles_head_request (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_ignores_query_params (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_includes_commit_sha_when_configured (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_omits_commit_sha_when_not_configured (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_returns_200 (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_returns_json (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_returns_ok_status (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_with_both_headers (core.tests.test_health.HealthCheckTestCase) ... ok
test_health_endpoint_with_request_id (core.tests.test_health.HealthCheckTestCase) ... ok

----------------------------------------------------------------------
Ran 26 tests in 0.053s

OK
Destroying test database for alias 'default'...
```

**Test breakdown:**

- 6 middleware tests
- 10 logging formatter tests
- 10 health endpoint tests
- **Total: 26 tests, all passing**

### Verification - Complete integration test

#### Manual end-to-end verification

**Start the server:**

```bash
cd travelmathlite
uv run python manage.py runserver 2>&1 | tee logs.json
```

**In another terminal, make a request:**

```bash
curl -H "X-Request-ID: manual-test-123" http://localhost:8000/health/
```

**Check the health response:**

```json
{"status":"ok"}
```

**Check the logs:**

```bash
tail -5 logs.json | jq .
```

**Expected log entry:**

```json
{
  "timestamp": "2025-11-19T20:15:30.456789+00:00",
  "level": "INFO",
  "module": "basehttp",
  "message": "GET /health/ HTTP/1.1 200",
  "request_id": "manual-test-123",
  "duration_ms": 2.45
}
```

**Verify all three features working together:**

1. ✅ **Middleware**: `request_id` is "manual-test-123" (from our header)
2. ✅ **Logging**: JSON format with all required fields
3. ✅ **Health endpoint**: HTTP 200 with `{"status":"ok"}`

---

## Summary

This tutorial covered the implementation of a complete observability stack for Django:

### What we built

1. **Request ID Middleware** (`core/middleware.py`)
   - Generates or reads `X-Request-ID` header
   - Tracks request duration in milliseconds
   - Attaches metadata to request object
   - Echoes request ID in response headers
   - Survives exceptions (INV-2)

2. **Structured JSON Logging** (`core/logging.py`)
   - Custom `JSONFormatter` for machine-readable logs
   - Includes request_id and duration_ms in every log
   - ISO 8601 timestamps with timezone
   - Exception tracebacks in JSON format
   - Configurable log levels via environment

3. **Health Check Endpoint** (`core/views.py`)
   - Simple `/health/` endpoint returning 200
   - Optional commit SHA header
   - No authentication required
   - Integrates with middleware for request tracking

4. **Comprehensive Testing**
   - 26 tests covering all features
   - Unit tests for middleware and logging
   - Integration tests for health endpoint
   - Test coverage for edge cases and exceptions

5. **Operations Documentation** (`docs/ops/logging-and-health.md`)
   - Usage examples and curl commands
   - Log analysis with jq
   - Troubleshooting guide
   - Integration examples (Kubernetes, Docker)

### Key learning outcomes

- **Middleware patterns**: Creating custom middleware with proper exception handling
- **Dynamic attributes**: Extending Django's request object safely
- **Custom logging formatters**: Implementing structured logging in Python
- **JSON serialization**: Creating machine-readable log output
- **Testing strategies**: Unit tests vs integration tests for different components
- **Environment-based configuration**: Using environment variables for operational settings

### Next steps

For production deployment, consider:

1. **Log aggregation**: Send JSON logs to a centralized logging system (ELK stack, CloudWatch, etc.)
2. **Monitoring**: Set up alerts based on log patterns and health endpoint status
3. **Distributed tracing**: Extend request ID pattern to trace across microservices
4. **Performance monitoring**: Use duration_ms for SLA tracking and performance analysis
5. **Security**: Review log contents to ensure no sensitive data is logged

### References

- **ADR-1.0.9**: `docs/travelmathlite/adr/adr-1.0.9-middleware-logging-and-request-id.md`
- **Briefs**: `docs/travelmathlite/briefs/adr-1.0.9/`
  - Brief-01: Request ID middleware
  - Brief-02: Structured logging
  - Brief-03: Health endpoint
  - Brief-04: Documentation and testing
- **Operations docs**: `docs/travelmathlite/ops/logging-and-health.md`
- **Django middleware docs**: <https://docs.djangoproject.com/en/5.2/topics/http/middleware/>
- **Python logging docs**: <https://docs.python.org/3/library/logging.html>
- **Django logging config**: <https://docs.djangoproject.com/en/5.2/topics/logging/>

---

## Quick command reference

```bash
# Run all observability tests
cd travelmathlite
uv run python manage.py test core.tests.test_middleware core.tests.test_logging core.tests.test_health

# Start server with logging to file
uv run python manage.py runserver 2>&1 | tee logs.json

# View logs with jq
tail -f logs.json | jq .

# Filter errors only
tail -f logs.json | jq 'select(.level == "ERROR")'

# Find slow requests
tail -f logs.json | jq 'select(.duration_ms > 100)'

# Test health endpoint
curl http://localhost:8000/health/

# Test with request ID
curl -H "X-Request-ID: test-123" http://localhost:8000/health/

# Set commit SHA
export LOG_COMMIT_SHA=$(git rev-parse HEAD)

# Check Django configuration
uv run python manage.py check --verbosity=2
```
