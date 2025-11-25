# TravelMathLite Testing Guide

This document describes the testing strategy and infrastructure for TravelMathLite, following ADR-1.0.11 (Testing Strategy).

## Overview

TravelMathLite uses Django's built-in TestCase framework (no pytest) with custom base classes to provide deterministic, isolated tests across all apps.

## Test Infrastructure

### Base Test Classes

Located in `apps/base/tests/base.py`, we provide three main test class types:

#### 1. BaseTestCase

The foundational test class with common setup and helper methods.

**Features:**

- RequestFactory for view testing
- User creation fixtures (regular and superuser)
- Common assertion helpers

**Example Usage:**

```python
from apps.base.tests import BaseTestCase

class MyViewTests(BaseTestCase):
    def test_calculator_view_get(self):
        # Create a test user
        user = self.create_user(username="testuser")
        
        # Make a request with RequestFactory
        request = self.make_request("GET", "/calculators/distance/", user=user)
        
        # Test your view
        response = DistanceView.as_view()(request)
        self.assertEqual(response.status_code, 200)
```

#### 2. MockingTestCase

Extends BaseTestCase with utilities for mocking external calls.

**Features:**

- Mock HTTP GET/POST requests
- Mock external APIs and functions
- Automatic mock cleanup after each test

**Example Usage:**

```python
from apps.base.tests import MockingTestCase

class DataImportTests(MockingTestCase):
    def test_import_airports_from_url(self):
        # Mock the HTTP GET request
        mock_data = {"airports": [{"code": "DFW", "name": "Dallas"}]}
        self.mock_http_get("https://example.com/airports.json", mock_data)
        
        # Run your import function
        result = import_airports_from_url("https://example.com/airports.json")
        
        # Verify behavior without hitting the real URL
        self.assertTrue(result.success)
```

#### 3. TimeTestCase

Extends BaseTestCase with helpers for time-sensitive testing.

**Features:**

- Freeze time for deterministic date/time tests
- Generate fixed timezone-aware datetimes
- Automatic mock cleanup

**Example Usage:**

```python
from apps.base.tests import TimeTestCase
from django.utils import timezone

class TimeBasedTests(TimeTestCase):
    def test_booking_expiration(self):
        # Freeze time to a specific moment
        fixed_time = self.get_fixed_datetime(2025, 11, 19, 12, 0, 0)
        self.freeze_time(fixed_time)
        
        # Test time-dependent logic
        booking = create_booking()
        self.assertEqual(booking.created_at, fixed_time)
```

## Running Tests

### Run All Tests

```bash
cd travelmathlite
uv run python manage.py test
```

### Run Tests for Specific App

```bash
uv run python manage.py test calculators
uv run python manage.py test search
uv run python manage.py test core.tests.test_health
```

### Run Specific Test Class or Method

```bash
uv run python manage.py test calculators.tests.DistanceCalculationTests
uv run python manage.py test calculators.tests.DistanceCalculationTests.test_valid_distance
```

## Testing Best Practices

### 1. Keep Tests Deterministic and Isolated

**Invariant INV-1:** Tests must be deterministic and isolated with no real network calls.

- Use mocking for external HTTP requests
- Use fixtures for test data (don't rely on database state)
- Freeze time for date/time dependent tests
- Clean up after each test

**Bad Example:**

```python
def test_weather_api(self):
    # DON'T: Makes real network call (non-deterministic)
    result = fetch_weather_from_api("https://api.weather.com")
    self.assertIsNotNone(result)
```

**Good Example:**

```python
def test_weather_api(self):
    # DO: Mock the external call
    mock_data = {"temp": 72, "conditions": "sunny"}
    self.mock_http_get("https://api.weather.com", mock_data)
    
    result = fetch_weather_from_api("https://api.weather.com")
    self.assertEqual(result["temp"], 72)
```

### 2. Test View Logic with RequestFactory

Use `make_request()` helper to test views without full HTTP overhead.

```python
def test_calculator_view_post(self):
    user = self.create_user()
    request = self.make_request(
        "POST",
        "/calculators/distance/",
        user=user,
        data={"origin": "DFW", "destination": "LAX"}
    )
    
    response = DistanceView.as_view()(request)
    self.assertEqual(response.status_code, 200)
```

### 3. Test HTMX Request Detection

**Invariant INV-2:** Same view handles both HTMX and full-page requests.

```python
def test_view_detects_htmx_request(self):
    # Test full-page request
    request_full = self.make_request("GET", "/search/")
    response_full = SearchView.as_view()(request_full)
    self.assertTemplateUsed(response_full, "search/results.html")
    
    # Test HTMX request
    request_htmx = self.make_request(
        "GET",
        "/search/",
        HTTP_HX_REQUEST="true"
    )
    response_htmx = SearchView.as_view()(request_htmx)
    self.assertTemplateUsed(response_htmx, "search/partials/results.html")
```

### 4. Mock External Dependencies

Always mock network calls, file I/O, and external APIs.

```python
from apps.base.tests import MockingTestCase

class ImportTests(MockingTestCase):
    def test_idempotent_import(self):
        # Mock the download
        csv_data = "code,name\nDFW,Dallas\nLAX,Los Angeles"
        self.mock_external_api(
            "apps.airports.utils.download_csv",
            return_value=csv_data
        )
        
        # First import
        import_airports()
        count1 = Airport.objects.count()
        
        # Second import (should be idempotent)
        import_airports()
        count2 = Airport.objects.count()
        
        self.assertEqual(count1, count2)
```

### 5. Use Fixtures for Test Data

Create helper methods for common test data patterns.

```python
class AirportTestCase(BaseTestCase):
    def create_airport(self, code="DFW", **kwargs):
        """Create a test airport deterministically."""
        defaults = {
            "name": f"{code} Airport",
            "city": "Test City",
            "country": "US",
            "latitude": 32.8998,
            "longitude": -97.0403,
        }
        defaults.update(kwargs)
        return Airport.objects.create(code=code, **defaults)
    
    def test_nearest_airport(self):
        # Use fixture
        dfw = self.create_airport("DFW")
        daa = self.create_airport("DAA", latitude=33.0, longitude=-97.0)
        
        # Test logic
        nearest = find_nearest_airport(32.9, -97.0)
        self.assertEqual(nearest.code, "DFW")
```

## Test Coverage Goals

Each app should have tests covering:

1. **Models:** Field validation, methods, constraints
2. **Views:** GET/POST handling, form validation, HTMX detection
3. **Forms:** Field validation, clean methods, error messages
4. **Business Logic:** Calculation functions, search algorithms
5. **Edge Cases:** Invalid inputs, boundary values, error conditions

## Visual Testing (Optional)

For behavioral validation, use Playwright scripts alongside unit tests:

```bash
# Run unit tests
uv run python manage.py test

# Run visual checks (optional)
uvx playwright install
uvx python scripts/visual_check.py
```

Visual checks capture screenshots and verify UI flows but do NOT replace unit tests.

## Continuous Integration

Tests run automatically on pull requests. Ensure:

- All tests pass locally before pushing
- Code is formatted with Ruff: `uv run ruff format .`
- No lint errors: `uv run ruff check .`

## Troubleshooting

### Tests Fail Intermittently

- **Cause:** Non-deterministic behavior (time, randomness, external calls)
- **Fix:** Use `freeze_time()` and mock all external dependencies

### Import Errors in Tests

- **Cause:** Circular imports or missing `__init__.py`
- **Fix:** Check import paths and ensure all test directories have `__init__.py`

### Database State Issues

- **Cause:** Tests not properly isolated
- **Fix:** Django TestCase automatically wraps each test in a transaction and rolls back; avoid manual transaction control

## References

- ADR-1.0.11: Testing Strategy
- PRD §4 F-011: Testing Requirements
- Django Testing Documentation: <https://docs.djangoproject.com/en/stable/topics/testing/>

---

**Last Updated:** November 19, 2025  
**Status:** Active  
**ADR:** adr-1.0.11-testing-strategy.md
