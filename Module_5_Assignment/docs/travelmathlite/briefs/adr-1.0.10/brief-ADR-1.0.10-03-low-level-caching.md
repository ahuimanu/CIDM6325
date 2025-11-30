# BRIEF: Implement low-level caching for computed data

Goal

- Use Django's low-level cache API to cache expensive computed data (airport lists, distance calculations) with appropriate cache keys and TTLs, addressing PRD §4 F-013 and §7 NF-001.

Scope (single PR)

- Files to touch:
  - `travelmathlite/apps/airports/utils.py` — Cache airport query results
  - `travelmathlite/apps/calculators/utils.py` — Cache expensive distance calculations
  - `travelmathlite/apps/airports/tests/test_cache_utils.py` — Tests for caching utilities
  - `travelmathlite/apps/calculators/tests/test_cache_utils.py` — Tests for calculator caching
- Non-goals: View-level caching (covered in brief-02), complex invalidation logic

Standards

- Commits: conventional style (feat: add low-level caching for computed data).
- Cache keys must be deterministic and include version/params in key.
- Django tests: use unittest/Django TestCase (no pytest).
- Document cache key patterns in code comments.

Acceptance

- Airport list queries cached with key based on filters
- Distance calculations cached with key based on coordinates
- Cache TTL: 900 seconds (15 minutes) for computed data
- Manual cache invalidation helper function available
- Tests verify cache hits/misses and key uniqueness
- Include migration? no
- Update docs: add low-level caching patterns to `docs/travelmathlite/ops/caching.md`

Prompts for Copilot

- "Add low-level caching to airport query functions in apps/airports/utils.py. Use django.core.cache with deterministic keys based on query parameters. TTL should be 900 seconds."
- "Add low-level caching to expensive distance calculations in apps/calculators/utils.py. Cache results with keys based on coordinate pairs (lat/lon)."
- "Create cache invalidation helper function clear_airport_cache() in apps/airports/utils.py that clears all airport-related cache keys (use cache key prefix pattern)."
- "Create tests that verify cache behavior: test cache hits, test cache misses, test key uniqueness, test TTL expiration, test manual invalidation."

Trace

- FR-F-013-1: Enable per-view/low-level caching on hot paths
- NF-001: Performance p95 targets
- INV-1: Cache TTLs respected; content varies by query params

Implementation notes

- Import: `from django.core.cache import cache`
- Cache key pattern: `travelmathlite:<module>:<function>:<params_hash>`
- Use `cache.get()`, `cache.set()`, `cache.delete()`, `cache.clear()`
- Use `cache.get_or_set()` for atomic fetch-or-compute
- Hash complex parameters (use `hashlib.md5` or simple string concatenation for simple cases)

Verification

```bash
cd travelmathlite

# Test low-level caching
uv run python manage.py shell -c "
from apps.airports.utils import get_airports_by_country
from django.core.cache import cache
import time

cache.clear()

# First call (cache miss)
start = time.time()
airports1 = get_airports_by_country('US')
time1 = time.time() - start

# Second call (cache hit)
start = time.time()
airports2 = get_airports_by_country('US')
time2 = time.time() - start

print(f'First call: {time1:.4f}s')
print(f'Second call: {time2:.4f}s')
print(f'Speedup: {time1/time2:.2f}x')
print(f'Results identical: {airports1 == airports2}')
"

# Test cache invalidation
uv run python manage.py shell -c "
from apps.airports.utils import clear_airport_cache
clear_airport_cache()
print('✓ Airport cache cleared')
"

# Run tests
uv run python manage.py test apps.airports.tests.test_cache_utils
uv run python manage.py test apps.calculators.tests.test_cache_utils
```

Example low-level caching implementation

```python
# apps/airports/utils.py
from django.core.cache import cache
import hashlib

CACHE_TTL = 900  # 15 minutes

def get_airports_by_country(country_code):
    """Get airports by country code with caching."""
    cache_key = f"travelmathlite:airports:country:{country_code}"
    
    # Try to get from cache
    airports = cache.get(cache_key)
    if airports is not None:
        return airports
    
    # Cache miss - compute and store
    airports = list(Airport.objects.filter(country_code=country_code))
    cache.set(cache_key, airports, CACHE_TTL)
    
    return airports

def get_airports_by_filters(country=None, city=None, iata=None):
    """Get airports by multiple filters with caching."""
    # Create deterministic cache key
    params = f"{country or ''}:{city or ''}:{iata or ''}"
    cache_key = f"travelmathlite:airports:filter:{params}"
    
    # Use get_or_set for atomic operation
    def compute_airports():
        queryset = Airport.objects.all()
        if country:
            queryset = queryset.filter(country_code=country)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if iata:
            queryset = queryset.filter(iata_code=iata)
        return list(queryset)
    
    return cache.get_or_set(cache_key, compute_airports, CACHE_TTL)

def clear_airport_cache():
    """Clear all airport-related cache keys."""
    # Note: This is a simple implementation. For production with many keys,
    # consider using cache key versioning or Redis SCAN/DELETE pattern.
    cache.delete_pattern("travelmathlite:airports:*")
```

Example distance calculation caching

```python
# apps/calculators/utils.py
from django.core.cache import cache
import hashlib

CACHE_TTL = 900  # 15 minutes

def haversine_distance_cached(lat1, lon1, lat2, lon2):
    """Calculate haversine distance with caching."""
    # Create deterministic cache key from coordinates
    # Round to 4 decimal places (~11m precision) to improve cache hits
    coords = f"{round(lat1,4)}:{round(lon1,4)}:{round(lat2,4)}:{round(lon2,4)}"
    cache_key = f"travelmathlite:distance:haversine:{coords}"
    
    # Try cache first
    distance = cache.get(cache_key)
    if distance is not None:
        return distance
    
    # Compute distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    
    # Cache result
    cache.set(cache_key, distance, CACHE_TTL)
    
    return distance

def get_nearest_airports_cached(lat, lon, limit=5):
    """Get nearest airports with caching."""
    coords = f"{round(lat,2)}:{round(lon,2)}:{limit}"
    cache_key = f"travelmathlite:nearest:airports:{coords}"
    
    def compute_nearest():
        # Expensive calculation
        return find_nearest_airports(lat, lon, limit)
    
    return cache.get_or_set(cache_key, compute_nearest, CACHE_TTL)
```

Test structure

```python
# apps/airports/tests/test_cache_utils.py
from django.test import TestCase
from django.core.cache import cache
from apps.airports.utils import get_airports_by_country, clear_airport_cache

class AirportCachingTestCase(TestCase):
    def setUp(self):
        cache.clear()
    
    def test_airports_cached_by_country(self):
        """Test that airport queries are cached."""
        # First call - cache miss
        airports1 = get_airports_by_country('US')
        
        # Second call - cache hit
        airports2 = get_airports_by_country('US')
        
        # Should return same results
        self.assertEqual(airports1, airports2)
    
    def test_different_countries_different_cache(self):
        """Test that different countries use different cache keys."""
        airports_us = get_airports_by_country('US')
        airports_uk = get_airports_by_country('UK')
        
        # Should not be identical
        self.assertNotEqual(airports_us, airports_uk)
    
    def test_cache_invalidation(self):
        """Test manual cache clearing."""
        # Cache some data
        get_airports_by_country('US')
        
        # Clear cache
        clear_airport_cache()
        
        # Verify cache is empty (would need to set a marker to test)
        # This is a simplified test
        cache_key = "travelmathlite:airports:country:US"
        self.assertIsNone(cache.get(cache_key))
```

Cache key patterns

- `travelmathlite:airports:country:{code}` — Airports by country
- `travelmathlite:airports:filter:{params}` — Filtered airport lists
- `travelmathlite:distance:haversine:{coords}` — Distance calculations
- `travelmathlite:nearest:airports:{lat}:{lon}:{limit}` — Nearest airports

Invalidation strategies

- **Time-based**: Let TTL expire (default)
- **Manual**: Call `clear_airport_cache()` after dataset imports
- **Versioned keys**: Include dataset version in key (future enhancement)
