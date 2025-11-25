# Logging and Health Endpoint Operations Guide

**Status:** Implemented per ADR-1.0.9  
**Last Updated:** 2025-11-19

## Overview

This document describes the observability features implemented for TravelMathLite:

1. **Request ID Middleware** - Unique identifier tracking for every request
2. **Structured JSON Logging** - Machine-readable logs with request metadata
3. **Health Endpoint** - Liveness checks for monitoring and load balancers

These features satisfy FR-F-015-1 (logging requirements) and NF-004 (reliability/observability).

---

## Request ID Middleware

### Purpose

The `RequestIDMiddleware` ensures every HTTP request has a unique identifier that can be traced through logs, making debugging and monitoring easier.

### Behavior

- **Reads** `X-Request-ID` header from incoming requests, or **generates** a UUID4 if not provided
- **Attaches** `request_id` and `duration_ms` attributes to the Django request object
- **Echoes** `X-Request-ID` in the response headers
- **Survives exceptions** to ensure timing information is always available

### Configuration

The middleware is configured in `travelmathlite/core/settings/base.py`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.RequestIDMiddleware",  # Early in stack
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ... other middleware
]
```

### Usage Example

**Send a request with your own request ID:**

```bash
curl -H "X-Request-ID: my-trace-123" http://localhost:8000/
```

**Send a request without request ID (one will be generated):**

```bash
curl http://localhost:8000/
```

Response will include:

```
X-Request-ID: <your-id-or-generated-uuid>
```

### Invariants

- **INV-1**: `request.request_id` is always present (never None)
- **INV-2**: `request.duration_ms` is logged even when exceptions occur

---

## Structured JSON Logging

### Purpose

All application logs are formatted as JSON lines for easy parsing, querying, and integration with log aggregation systems.

### Log Format

Each log entry is a single JSON line with the following fields:

```json
{
  "timestamp": "2025-11-19T19:30:45.123456+00:00",
  "level": "INFO",
  "module": "views",
  "message": "User logged in successfully",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "duration_ms": 45.23
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | ISO 8601 timestamp with timezone (UTC) |
| `level` | string | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `module` | string | Python module where the log originated |
| `message` | string | Formatted log message |
| `request_id` | string | Request ID from middleware (or "-" if not in request context) |
| `duration_ms` | float/null | Request duration in milliseconds (or null if not in request context) |
| `exc_info` | string | Exception traceback (only present when logging exceptions) |

### Configuration

Logging is configured in `travelmathlite/core/settings/base.py`:

```python
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
}
```

### Environment Variables

- `LOG_LEVEL` - Root logger level (default: INFO)
- `DJANGO_LOG_LEVEL` - Django framework logger level (default: INFO)

### Viewing Logs

**Run the development server and watch logs:**

```bash
cd travelmathlite
uv run python manage.py runserver 2>&1 | tee logs.json
```

**Filter logs by level:**

```bash
tail -f logs.json | jq 'select(.level == "ERROR")'
```

**Extract request IDs:**

```bash
tail -f logs.json | jq -r '.request_id' | grep -v "^-$"
```

**Show requests slower than 100ms:**

```bash
tail -f logs.json | jq 'select(.duration_ms > 100)'
```

**View last 10 logs with pretty formatting:**

```bash
tail -10 logs.json | jq .
```

### Invariants

- **INV-3**: Logs include `duration_ms` field (even if null when outside request context)

---

## Health Endpoint

### Purpose

The `/health/` endpoint provides a simple liveness check for monitoring systems, load balancers, and orchestration platforms (Kubernetes, Docker, etc.).

### Endpoint Details

- **URL:** `/health/`
- **Method:** GET, HEAD
- **Authentication:** None (public endpoint)
- **Response:** HTTP 200 with JSON payload

### Response Format

**Basic response:**

```json
{"status": "ok"}
```

**Response headers:**

```
Content-Type: application/json
X-Request-ID: <request-id-from-middleware>
X-Commit-SHA: <git-commit-sha>  (only if LOG_COMMIT_SHA env var is set)
```

### Usage Examples

**Basic health check:**

```bash
curl http://localhost:8000/health/
```

Output:

```json
{"status":"ok"}
```

**Health check with request ID:**

```bash
curl -H "X-Request-ID: health-check-123" http://localhost:8000/health/
```

**Health check with verbose headers:**

```bash
curl -v http://localhost:8000/health/
```

Output includes:

```
< HTTP/1.1 200 OK
< Content-Type: application/json
< X-Request-ID: <uuid>
< X-Commit-SHA: abc123def456  (if configured)
...
{"status":"ok"}
```

**HEAD request (for lightweight checks):**

```bash
curl -I http://localhost:8000/health/
```

### Configuration

**Enable commit SHA header (optional):**

```bash
export LOG_COMMIT_SHA=$(git rev-parse HEAD)
```

Then restart the server. The health endpoint will include the `X-Commit-SHA` header.

### Use Cases

**Kubernetes liveness probe:**

```yaml
livenessProbe:
  httpGet:
    path: /health/
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

**Docker Compose healthcheck:**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 3s
  retries: 3
```

**Load balancer health check:**

```bash
# AWS ALB, Google Cloud Load Balancer, etc.
# Configure health check path: /health/
# Expected status: 200
```

### Invariants

- **INV-2**: Health endpoint always returns HTTP 200 (even during partial outages)

---

## Testing

### Running Tests

All observability features have comprehensive test coverage.

**Run all core tests (middleware, logging, health):**

```bash
cd travelmathlite
uv run python manage.py test core.tests.test_middleware core.tests.test_logging core.tests.test_health
```

**Run individual test suites:**

```bash
# Middleware tests (6 tests)
uv run python manage.py test core.tests.test_middleware

# Logging tests (10 tests)
uv run python manage.py test core.tests.test_logging

# Health endpoint tests (10 tests)
uv run python manage.py test core.tests.test_health
```

### Test Coverage

**Middleware Tests** (`core.tests.test_middleware`)

- Request ID generation when not provided
- Request ID passthrough from headers
- Duration calculation in milliseconds
- Exception handling (INV-2)
- Request ID persistence through middleware chain
- Unique ID generation for different requests

**Logging Tests** (`core.tests.test_logging`)

- Valid JSON output format
- Required fields presence
- Request ID extraction from log record
- Duration extraction from log record
- Fallback behavior (request_id → "-", duration_ms → null)
- Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Exception information handling
- Handler integration
- Message formatting with arguments
- Silent test execution (no console output)

**Health Endpoint Tests** (`core.tests.test_health`)

- HTTP 200 response
- JSON content type and payload
- X-Commit-SHA header when `LOG_COMMIT_SHA` is set
- X-Commit-SHA omission when not configured
- Integration with request ID middleware
- Accessible without authentication
- HEAD request support
- Query parameter handling
- Combined headers (X-Request-ID + X-Commit-SHA)

### Expected Output

All tests should pass with output similar to:

```
Found 26 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.051s

OK
Destroying test database for alias 'default'...
```

### Continuous Integration

These tests should be run in CI/CD pipelines before deployment:

```bash
# In your CI script
cd travelmathlite
uv run python manage.py test core.tests.test_middleware core.tests.test_logging core.tests.test_health --verbosity=2
```

---

## Troubleshooting

### Request ID Not Appearing in Logs

**Problem:** Logs show `request_id: "-"` instead of UUID.

**Solution:** Ensure `RequestIDMiddleware` is enabled and positioned early in the middleware stack. Check `MIDDLEWARE` setting in `core/settings/base.py`.

### Logs Not in JSON Format

**Problem:** Logs appear as plain text instead of JSON.

**Solution:** Verify the `LOGGING` configuration uses `core.logging.JSONFormatter`. Check that you're running with the correct settings module.

### Health Endpoint Returns 404

**Problem:** `/health/` returns 404 Not Found.

**Solution:** Ensure `core.urls` includes the health endpoint route:

```python
path("health/", health_check, name="health"),
```

### Commit SHA Not Appearing in Health Response

**Problem:** `X-Commit-SHA` header is missing from `/health/` response.

**Solution:** Set the `LOG_COMMIT_SHA` environment variable:

```bash
export LOG_COMMIT_SHA=$(git rev-parse HEAD)
```

Then restart the Django server.

### Duration Always Null in Logs

**Problem:** `duration_ms` is always `null` in logs.

**Solution:** This is expected for logs outside of request context (e.g., startup logs, management commands). For request-related logs, ensure middleware is properly configured.

---

## Performance Considerations

### Middleware Overhead

The request ID middleware adds minimal overhead:

- **UUID generation:** ~1-2 microseconds
- **Header reading/writing:** negligible
- **Timing:** ~1 microsecond (using `time.perf_counter()`)

**Total overhead:** < 5 microseconds per request

### Logging Performance

JSON serialization is fast but has some overhead:

- Use appropriate `LOG_LEVEL` in production (INFO or WARNING)
- Avoid excessive logging in hot code paths
- Consider log sampling for high-traffic endpoints

### Health Endpoint

The health endpoint is extremely lightweight:

- No database queries
- No external service calls
- Simple JSON serialization
- **Response time:** < 1ms typically

---

## Security Considerations

### Request ID Validation

Request IDs from headers are accepted as-is (any string). While this is generally safe, be aware:

- Request IDs appear in logs and headers
- Don't include sensitive data in request IDs
- Log analysis tools should handle arbitrary strings

### Health Endpoint

The health endpoint is intentionally public:

- No authentication required (by design)
- No sensitive information exposed
- Only returns `{"status": "ok"}` and optional commit SHA
- Suitable for external monitoring

### Commit SHA Disclosure

The `X-Commit-SHA` header (when enabled) discloses:

- Git commit hash
- Deployment version information

This is generally safe and useful for debugging, but consider:

- Some organizations prefer not to expose version info publicly
- Use `LOG_COMMIT_SHA` selectively (e.g., internal health checks only)

---

## References

- **ADR-1.0.9:** Architecture Decision Record for middleware, logging, and health endpoint
- **PRD FR-F-015-1:** Logging requirements
- **PRD NF-004:** Reliability and observability requirements
- **Brief-01:** Request ID middleware implementation
- **Brief-02:** Structured JSON logging implementation
- **Brief-03:** Health endpoint implementation

---

## Maintenance

### Updating Log Fields

To add new fields to JSON logs, modify `core/logging.py`:

```python
# In JSONFormatter.format()
log_entry = {
    "timestamp": datetime.now(UTC).isoformat(),
    "level": record.levelname,
    "module": record.module,
    "message": record.getMessage(),
    "request_id": request_id,
    "duration_ms": duration_ms,
    "new_field": value,  # Add new field here
}
```

### Changing Health Endpoint Response

To modify the health endpoint response, edit `core/views.py`:

```python
def health_check(request):
    response = JsonResponse({
        "status": "ok",
        "version": "1.0.0",  # Add version info
        "timestamp": datetime.now(UTC).isoformat(),  # Add timestamp
    })
    # ... rest of the function
```

Remember to update tests accordingly.

---

## Quick Command Reference

```bash
# Run all observability tests
uv run python manage.py test core.tests.test_middleware core.tests.test_logging core.tests.test_health

# Start server with logging
uv run python manage.py runserver 2>&1 | tee logs.json

# Health check
curl http://localhost:8000/health/

# Health check with request ID
curl -H "X-Request-ID: test-123" http://localhost:8000/health/

# View logs with jq
tail -f logs.json | jq .

# Filter errors only
tail -f logs.json | jq 'select(.level == "ERROR")'

# Find slow requests (>100ms)
tail -f logs.json | jq 'select(.duration_ms > 100)'

# Set commit SHA for health endpoint
export LOG_COMMIT_SHA=$(git rev-parse HEAD)
```
