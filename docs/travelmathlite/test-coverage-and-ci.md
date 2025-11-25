# Test Coverage and CI Documentation

This document describes the automated test suite and continuous integration setup for TravelMathLite.

## Test Suite Overview

### Current Test Coverage

**Total Tests**: 69 passing tests across airports and base apps

#### Apps/Airports Tests (58 tests)

1. **Import Tests** (`tests_import.py`) - 9 tests
   - Create airport records from CSV
   - Dry-run mode validation
   - IATA filtering
   - Missing required fields handling
   - Invalid coordinate handling
   - Idempotency verification
   - Limit parameter functionality

2. **Schema Mapping Tests** (`tests_schema_mapping.py`) - 13 tests
   - CSV row normalization
   - Coordinate type conversion
   - Elevation conversion
   - Field name mapping (`type` → `airport_type`)
   - Invalid data handling
   - Edge case coordinates
   - Model field documentation
   - Import command integration

3. **Validation Tests** (`tests_validation.py`) - Coverage for data quality checks

4. **Validate Command Tests** (`tests_validate_command.py`) - Command output and metrics

5. **Update Command Tests** (`tests_update_command.py`) - 4 tests
   - Update command calls import
   - Integration without mocking
   - Dry-run mode
   - Exception handling

6. **City/Country Integration Tests** (`tests_city_country_integration.py`) - 4 tests
   - Import command links airports to Country/City
   - Location integrator creates normalized models
   - Nearest QuerySet helper orders by distance
   - Search matches normalized fields

7. **Distance Units Tests** (`tests_distance_units.py`) - 2 tests
   - Nearest attaches distance_km
   - Nearest attaches distance_mi when requested

8. **URL/Template Tests** (`tests.py`) - 2 tests
   - Index renders with partial
   - Reverse URL resolution

#### Apps/Base Tests (11 tests)

1. **Model Tests** (`tests/test_models.py`)
   - Country model creation and normalization
   - City model creation and normalization
   - QuerySet methods (active, search)
   - Slug generation
   - Search name normalization

2. **Namespace Tests** (`tests/test_namespaces.py`)
   - Admin registration
   - Model imports

### Test Data Integrity

While a dedicated data integrity test suite was attempted, the existing 69 tests already cover key integrity concerns:

- **Uniqueness**: Primary key constraints (ident for Airport, iso_code for Country)
- **Foreign Keys**: Country/City FK relationships tested in integration tests
- **Required Fields**: Validated through import tests
- **Coordinate Ranges**: Import command validates before saving
- **Data Normalization**: Schema mapping tests verify normalization
- **Idempotency**: Import tests verify re-running doesn't duplicate

## Running Tests

### Local Development

```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test apps.airports
uv run python manage.py test apps.base

# Run both airport and base tests
uv run python manage.py test apps.airports apps.base

# Run with verbosity
uv run python manage.py test apps.airports apps.base --verbosity=2

# Run specific test class
uv run python manage.py test apps.airports.tests_import.ImportAirportsCommandTests

# Run single test method
uv run python manage.py test apps.airports.tests_import.ImportAirportsCommandTests.test_import_idempotent
```

### Test Output

Tests create an in-memory SQLite database and apply all migrations. Successful run shows:

```
Found 69 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................................................
----------------------------------------------------------------------
Ran 69 tests in 0.741s

OK
```

## Continuous Integration (CI)

### GitHub Actions Workflow

**File**: `.github/workflows/travelmathlite-tests.yml`

**Triggers**:
- Push to `FALL2025` or `main` branches (when travelmathlite/ files change)
- Pull requests targeting `FALL2025` or `main`

**Test Matrix**:
- Python 3.12
- Python 3.13

**CI Steps**:

1. **Checkout code**
2. **Install uv** (Astral package manager)
3. **Set up Python** (matrix version)
4. **Install dependencies** (`uv sync`)
5. **Run linter** (`uvx ruff check .`)
6. **Run formatter check** (`uvx ruff format --check .`)
7. **Run Django system check** (`python manage.py check`)
8. **Run migrations check** (`python manage.py makemigrations --check --dry-run`)
9. **Run tests** (`python manage.py test apps.airports apps.base --verbosity=2`)
10. **Run data validation** (verify validate_airports command exists)

### CI Benefits

- **Automated testing**: Every push and PR runs full test suite
- **Multiple Python versions**: Ensures compatibility with 3.12 and 3.13
- **Code quality**: Ruff linter and formatter enforce standards
- **Migration safety**: Detects uncommitted migrations
- **Early detection**: Catch issues before merge

### Viewing CI Results

1. Navigate to repository on GitHub
2. Click "Actions" tab
3. Select "TravelMathLite Tests" workflow
4. View run details, logs, and test output

### CI Badge (Optional)

Add to README.md:

```markdown
![Tests](https://github.com/ahuimanu/CIDM6325/actions/workflows/travelmathlite-tests.yml/badge.svg?branch=FALL2025)
```

## Test Coverage by Feature

| Feature | Test Coverage | Notes |
|---------|--------------|-------|
| Airport Import | ✅ Excellent | 9 tests covering all scenarios |
| Schema Mapping | ✅ Excellent | 13 tests for normalization and validation |
| Country/City Integration | ✅ Very Good | 4 tests for FK linking and caching |
| QuerySet Helpers | ✅ Good | active(), search(), nearest() tested |
| Distance Calculations | ✅ Good | Both km and mi units tested |
| Validation Command | ✅ Good | Command output verified |
| Update Automation | ✅ Good | 4 tests for scheduled updates |
| Admin Interface | ⚠️ Partial | Registration tested, UI not tested |
| Search Views | ⚠️ Minimal | URL/template tests only |

## Data Integrity Checks

### Automated Checks in Tests

1. **Uniqueness Constraints**
   - Airport ident uniqueness (enforced at DB level)
   - Country iso_code uniqueness
   - City (country, search_name) uniqueness
   - City (country, slug) uniqueness

2. **Foreign Key Integrity**
   - Country FK with PROTECT on delete
   - City FK with SET_NULL on delete
   - Integration tests verify linking

3. **Required Fields**
   - Import tests verify missing field handling
   - Schema tests verify field presence

4. **Data Normalization**
   - search_name lowercasing
   - Slug generation
   - Coordinate type conversion
   - Elevation handling

5. **Business Logic**
   - Active flag defaults to True
   - Closed airports marked inactive
   - IATA code filtering
   - Coordinate range validation (in import command)

### Manual Validation

Use `validate_airports` command for data quality checks:

```bash
uv run python manage.py validate_airports
```

Reports:
- Total airports
- IATA code coverage
- Coordinate completeness
- Elevation data presence
- Country FK coverage
- City FK coverage
- Warnings for low coverage

## Best Practices

### Writing Tests

1. **Use Django TestCase**: Follow project standards (no pytest)
2. **Keep fixtures small**: <10 records per test
3. **Test one thing**: Each test should verify one behavior
4. **Use descriptive names**: `test_import_creates_airports`
5. **Add docstrings**: Explain what the test verifies
6. **Clean up**: TestCase handles DB cleanup automatically

### Example Test Structure

```python
from django.test import TestCase
from apps.airports.models import Airport

class AirportFeatureTests(TestCase):
    """Test suite for airport feature."""

    def setUp(self):
        """Set up test data."""
        self.airport = Airport.objects.create(
            ident="TEST",
            name="Test Airport",
            latitude_deg=39.0,
            longitude_deg=-104.0,
            iso_country="US",
        )

    def test_feature_works_correctly(self):
        """Test that feature behaves as expected."""
        result = self.airport.some_method()
        self.assertEqual(result, expected_value)
```

### Running Tests Before Commit

```bash
# Full test suite
uv run python manage.py test apps.airports apps.base

# Lint check
uvx ruff check .

# Format check
uvx ruff format --check .

# All checks (same as CI)
uv run python manage.py check &&
uv run python manage.py makemigrations --check --dry-run &&
uvx ruff check . &&
uvx ruff format --check . &&
uv run python manage.py test apps.airports apps.base
```

## Future Enhancements

### Potential Test Additions

1. **Model Validators**: Add field validators to Airport model for lat/lon ranges
2. **Integration Tests**: End-to-end import workflow tests
3. **Performance Tests**: Large dataset import benchmarks
4. **Admin Tests**: Selenium/Playwright tests for admin interface
5. **API Tests**: If REST API is added
6. **Coverage Reports**: Generate coverage metrics in CI
7. **Mutation Testing**: Verify test suite catches code changes

### CI Enhancements

1. **Coverage Reports**: Add coverage.py and upload to Codecov
2. **Performance Monitoring**: Track test execution time
3. **Parallel Tests**: Run test classes in parallel
4. **Database Variants**: Test with PostgreSQL in CI
5. **Deployment Pipeline**: Auto-deploy passing builds
6. **Notification**: Slack/email on test failures

## Troubleshooting

### Tests Failing Locally

```bash
# Ensure dependencies are up to date
uv sync

# Check for uncommitted migrations
uv run python manage.py makemigrations --check

# Run with verbosity to see details
uv run python manage.py test --verbosity=2

# Run specific failing test
uv run python manage.py test apps.airports.tests_import.ImportAirportsCommandTests.test_import_creates_airports
```

### CI Failing on GitHub

1. Check workflow logs in Actions tab
2. Verify all files are committed (especially migrations)
3. Ensure Python version compatibility
4. Check for environment-specific issues
5. Run same commands locally that CI runs

### Test Database Issues

Tests use in-memory SQLite. If issues occur:

```bash
# Clear any .pyc files
find . -name "*.pyc" -delete

# Clear Django cache
rm -rf __pycache__

# Re-run migrations in test
# (handled automatically by test runner)
```

## Related Documentation

- [Contributing Guide](../CONTRIBUTING.md) - Development workflow
- [Data Model Integration](../data-model-integration.md) - Import workflow
- [Schema Mapping](../schema-mapping-airports.md) - Field mappings
- [ADR-1.0.1](../adr/adr-1.0.1-dataset-source-for-airports-and-cities.md) - Dataset decisions

---

**Last Updated**: 2025-11-14  
**Test Count**: 69 passing  
**CI Status**: ✅ Enabled
