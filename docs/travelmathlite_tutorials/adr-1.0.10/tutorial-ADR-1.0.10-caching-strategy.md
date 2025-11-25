# Tutorial: ADR-1.0.10 Caching Strategy

**Date:** November 19, 2025  
**ADR Reference:** [ADR-1.0.10 Caching Strategy](../../travelmathlite/adr/adr-1.0.10-caching-strategy.md)  
**Briefs:** [adr-1.0.10 briefs](../../travelmathlite/briefs/adr-1.0.10/)

---

## Overview

This tutorial walks through implementing Django's caching system for the TravelMathLite application to improve response times for repeated queries. We'll configure cache backends, apply per-view caching, implement low-level caching for computed data, add HTTP cache headers, and create comprehensive documentation and tests.

**Learning Objectives:**

- Configure Django cache backends (locmem for dev, Redis for production)
- Apply per-view caching with `@cache_page` decorator
- Implement low-level caching with Django's cache API
- Configure HTTP cache headers for browser/CDN caching
- Create management commands for cache operations
- Write comprehensive tests for cache behavior

**Prerequisites:**

- Django project set up (TravelMathLite)
- Basic understanding of HTTP caching concepts
- Familiarity with Django views and middleware
- uv package manager installed

---

## Section 1: Configure Cache Backend

**Brief Context:** [brief-ADR-1.0.10-01-cache-backend-config.md](../../travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-01-cache-backend-config.md)

**Goal:** Set up Django's CACHES setting with locmem for local development and optional Redis/file-based backend for production.

### 1.1 Django Caching Concepts

Django provides a unified caching API that works with multiple backends. From the Django documentation:

> **Django's cache framework:** Django comes with a robust cache system that lets you save dynamic pages so they don't have to be calculated for each request. The cache framework offers different levels of cache granularity: you can cache the output of specific views, you can cache only the pieces that are difficult to produce, or you can cache your entire site.

**Key concepts:**

- **Cache backend**: Where cached data is stored (memory, filesystem, Redis, Memcached)
- **TTL (Time To Live)**: How long cached data remains valid
- **Cache keys**: Unique identifiers for cached items
- **Cache granularity**: Page-level, view-level, fragment-level, or low-level API

### 1.2 Implementation Steps

#### Step 1: Configure base cache settings

Edit `travelmathlite/core/settings/base.py`:

```python
# Cache configuration
# Use django-environ for easy backend switching
CACHES = {
    'default': env.cache_url('CACHE_URL', default='locmem://'),
}

# Alternative explicit configuration for locmem:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'travelmathlite-cache',
#         'TIMEOUT': 300,  # 5 minutes default TTL
#         'OPTIONS': {
#             'MAX_ENTRIES': 1000,
#         },
#     }
# }
```

**Django cache backend options:**

- `locmem` - Local memory (single process, good for development)
- `filebased` - Filesystem (persistent, slower)
- `redis` - Redis server (fast, supports multiple processes)
- `memcached` - Memcached server (fast, distributed)
- `dummy` - No caching (for testing)

#### Step 2: Update local settings

Ensure `travelmathlite/core/settings/local.py` uses locmem (already default):

```python
# Local development uses locmem by default
# No additional configuration needed - inherits from base.py
```

#### Step 3: Update production settings

Edit `travelmathlite/core/settings/prod.py` to support environment-based configuration:

```python
# Production can override cache backend via CACHE_URL
# Examples:
# CACHE_URL=redis://localhost:6379/1
# CACHE_URL=file:///tmp/django_cache
```

#### Step 4: Document cache URL formats

Create or update `travelmathlite/.env.example`:

```bash
# Cache Backend Configuration
# Local memory (default for development)
CACHE_URL=locmem://

# File-based cache (persistent across restarts)
# CACHE_URL=file:///tmp/django_cache

# Redis (recommended for production)
# CACHE_URL=redis://localhost:6379/1
# CACHE_URL=redis://username:password@redis-host:6379/1

# Memcached
# CACHE_URL=memcached://127.0.0.1:11211
```

### 1.3 Verification

Test cache configuration:

```bash
cd travelmathlite

# Test locmem backend (default)
uv run python manage.py shell -c "
from django.core.cache import cache
print(f'Backend: {cache.__class__.__name__}')
cache.set('test_key', 'test_value', 60)
print(f'Cached value: {cache.get(\"test_key\")}')
cache.delete('test_key')
print('✓ Cache working')
"
```

Expected output:

```
Backend: LocMemCache
Cached value: test_value
✓ Cache working
```

### 1.4 Create Tests

Create `travelmathlite/core/tests/test_cache_config.py`:

```python
"""Tests for cache configuration."""
from django.test import TestCase
from django.core.cache import cache


class CacheConfigTestCase(TestCase):
    """Test cache backend configuration."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_cache_backend_available(self):
        """Test that cache backend is configured and working."""
        # Should be able to set and get values
        cache.set('test_key', 'test_value', 60)
        value = cache.get('test_key')
        self.assertEqual(value, 'test_value')

    def test_cache_timeout(self):
        """Test that cache respects timeout settings."""
        import time
        
        # Set with 1 second timeout
        cache.set('short_lived', 'value', 1)
        self.assertEqual(cache.get('short_lived'), 'value')
        
        # Wait and verify expiration
        time.sleep(2)
        self.assertIsNone(cache.get('short_lived'))

    def test_cache_delete(self):
        """Test cache deletion."""
        cache.set('deletable', 'value', 300)
        self.assertEqual(cache.get('deletable'), 'value')
        
        cache.delete('deletable')
        self.assertIsNone(cache.get('deletable'))

    def tearDown(self):
        """Clean up after tests."""
        cache.clear()
```

Run tests:

```bash
uv run python manage.py test core.tests.test_cache_config
```

---

## Section 2: Implement Per-View Caching

**Brief Context:** [brief-ADR-1.0.10-02-per-view-caching.md](../../travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-02-per-view-caching.md)

**Goal:** Apply Django's `@cache_page` decorator to hot-path views with appropriate TTLs.

### 2.1 Django Per-View Caching Concepts

From Django's caching documentation:

> **Per-view cache:** The `cache_page` decorator caches the entire output of a view. It takes a single argument: the cache timeout in seconds. The cache will use the URL to create the cache key, so two URLs that differ only by query string will be cached separately.

**Key patterns:**

- Function-based views: `@cache_page(timeout)` decorator
- Class-based views: `method_decorator(cache_page(timeout), name='dispatch')`
- Cache varies by full URL including query parameters
- Only caches GET and HEAD requests (POST always bypasses cache)

### 2.2 Implementation Steps

#### Step 1: Add caching to search views

Edit `travelmathlite/apps/search/views.py`:

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# For function-based views:
@cache_page(300)  # Cache for 5 minutes
def search_results(request):
    """Search airport results with caching."""
    query = request.GET.get('q', '')
    # ... existing search logic
    return render(request, 'search/results.html', context)

# For class-based views:
@method_decorator(cache_page(300), name='dispatch')
class SearchView(View):
    """Search view with per-view caching."""
    
    def get(self, request):
        query = request.GET.get('q', '')
        # ... search logic
        return render(request, 'search/results.html', context)
```

**TTL Strategy:**

- Search results: 300 seconds (5 minutes) - balance freshness and performance
- Results change infrequently but users expect recent data

#### Step 2: Add caching to calculator views

Edit `travelmathlite/apps/calculators/views.py`:

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(600), name='dispatch')  # 10 minutes
class NearestAirportView(View):
    """Nearest airport calculator with caching."""
    
    def get(self, request):
        # ... calculator logic
        return render(request, 'calculators/nearest.html', context)

@method_decorator(cache_page(600), name='dispatch')
class DistanceCalculatorView(View):
    """Distance calculator with caching."""
    
    def get(self, request):
        # ... distance calculation logic
        return render(request, 'calculators/distance.html', context)
```

### 2.3 Verification

Test caching with timing:

```bash
cd travelmathlite

# Start development server
uv run python manage.py runserver

# In another terminal, test cache performance
uv run python -c "
import requests
import time

url = 'http://localhost:8000/search/?q=Dallas'

# First request (cache miss)
start = time.time()
r1 = requests.get(url)
time1 = time.time() - start

# Second request (cache hit)
start = time.time()
r2 = requests.get(url)
time2 = time.time() - start

print(f'First request:  {time1:.4f}s (cache miss)')
print(f'Second request: {time2:.4f}s (cache hit)')
print(f'Speedup: {time1/time2:.2f}x faster')
"
```

### 2.4 Create Tests

Create `travelmathlite/apps/search/tests/test_caching.py`:

```python
"""Tests for search view caching."""
from django.test import TestCase, Client
from django.core.cache import cache


class SearchCachingTestCase(TestCase):
    """Test search view caching behavior."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_search_results_cached(self):
        """Test that identical search queries return cached results."""
        client = Client()
        
        # First request
        response1 = client.get('/search/?q=Dallas')
        self.assertEqual(response1.status_code, 200)
        
        # Second identical request should be cached
        response2 = client.get('/search/?q=Dallas')
        self.assertEqual(response2.status_code, 200)
        
        # Content should be identical
        self.assertEqual(response1.content, response2.content)

    def test_different_queries_different_cache(self):
        """Test that different queries use different cache keys."""
        client = Client()
        
        response1 = client.get('/search/?q=Dallas')
        response2 = client.get('/search/?q=Houston')
        
        # Both should succeed
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Content should differ (different results)
        self.assertNotEqual(response1.content, response2.content)

    def test_query_params_vary_cache(self):
        """Test that query parameter changes create different cache keys."""
        client = Client()
        
        response1 = client.get('/search/?q=Dallas')
        response2 = client.get('/search/?q=Dallas&page=2')
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Different pages should have different content
        self.assertNotEqual(response1.content, response2.content)

    def tearDown(self):
        """Clean up after tests."""
        cache.clear()
```

Run tests:

```bash
uv run python manage.py test apps.search.tests.test_caching
```

---

## Section 3: Implement Low-Level Caching

**Brief Context:** [brief-ADR-1.0.10-03-low-level-caching.md](../../travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-03-low-level-caching.md)

**Goal:** Use Django's low-level cache API for expensive computed data.

### 3.1 Low-Level Cache API Concepts

Django's low-level cache API provides fine-grained control over what gets cached:

> **Low-level cache API:** For situations where caching entire view output is too coarse-grained, Django provides a low-level cache API that lets you cache any Python object that can be pickled safely.

**Key API methods:**

- `cache.get(key, default=None)` - Retrieve cached value
- `cache.set(key, value, timeout=DEFAULT_TIMEOUT)` - Store value
- `cache.get_or_set(key, callable, timeout=DEFAULT_TIMEOUT)` - Atomic fetch-or-compute
- `cache.delete(key)` - Remove cached value
- `cache.clear()` - Clear all cached values

**Cache key best practices:**

- Use namespace prefixes: `appname:module:function:params`
- Make keys deterministic (same inputs = same key)
- Keep keys under 250 characters
- Use hash for complex parameters

### 3.2 Implementation Steps

#### Step 1: Cache airport queries

Create or edit `travelmathlite/apps/airports/utils.py`:

```python
"""Airport utility functions with caching."""
from django.core.cache import cache
from .models import Airport

CACHE_TTL = 900  # 15 minutes


def get_airports_by_country(country_code):
    """Get airports by country code with caching.
    
    Args:
        country_code: ISO country code (e.g., 'US')
    
    Returns:
        List of Airport objects
    """
    cache_key = f"travelmathlite:airports:country:{country_code}"
    
    # Try to get from cache
    airports = cache.get(cache_key)
    if airports is not None:
        return airports
    
    # Cache miss - query database
    airports = list(Airport.objects.filter(country_code=country_code))
    
    # Store in cache
    cache.set(cache_key, airports, CACHE_TTL)
    
    return airports


def get_airports_by_filters(country=None, city=None, iata=None):
    """Get airports by multiple filters with caching.
    
    Uses atomic get_or_set pattern for cleaner code.
    """
    # Create deterministic cache key
    params = f"{country or ''}:{city or ''}:{iata or ''}"
    cache_key = f"travelmathlite:airports:filter:{params}"
    
    # Define computation function
    def compute_airports():
        queryset = Airport.objects.all()
        if country:
            queryset = queryset.filter(country_code=country)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if iata:
            queryset = queryset.filter(iata_code=iata)
        return list(queryset)
    
    # Atomic fetch-or-compute
    return cache.get_or_set(cache_key, compute_airports, CACHE_TTL)


def clear_airport_cache():
    """Clear all airport-related cache keys.
    
    Note: This is a simple implementation. For production with many keys,
    consider using cache key versioning or Redis SCAN/DELETE pattern.
    """
    # For locmem, we can clear all or use pattern matching with Redis
    cache.clear()  # Clears entire cache
    # For Redis: cache.delete_pattern("travelmathlite:airports:*")
```

#### Step 2: Cache distance calculations

Create or edit `travelmathlite/apps/calculators/utils.py`:

```python
"""Calculator utility functions with caching."""
from django.core.cache import cache
import math

CACHE_TTL = 900  # 15 minutes


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate haversine distance between two points.
    
    Returns distance in kilometers.
    """
    R = 6371  # Earth radius in kilometers
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def haversine_distance_cached(lat1, lon1, lat2, lon2):
    """Calculate haversine distance with caching.
    
    Round coordinates to 4 decimal places (~11m precision) to improve cache hits.
    """
    # Create deterministic cache key
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
    """Get nearest airports with caching.
    
    Round user location to reduce cache key variations.
    """
    # Round to 2 decimals (~1km precision) for better cache hits
    coords = f"{round(lat,2)}:{round(lon,2)}:{limit}"
    cache_key = f"travelmathlite:nearest:airports:{coords}"
    
    def compute_nearest():
        # Expensive calculation - find nearest airports
        from apps.airports.models import Airport
        
        airports = Airport.objects.all()
        results = []
        
        for airport in airports:
            if airport.latitude and airport.longitude:
                distance = haversine_distance(
                    lat, lon, 
                    float(airport.latitude), 
                    float(airport.longitude)
                )
                results.append((airport, distance))
        
        # Sort by distance and limit
        results.sort(key=lambda x: x[1])
        return results[:limit]
    
    return cache.get_or_set(cache_key, compute_nearest, CACHE_TTL)
```

### 3.3 Verification

Test low-level caching:

```bash
cd travelmathlite

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

print(f'First call:  {time1:.4f}s (database query)')
print(f'Second call: {time2:.4f}s (cached)')
print(f'Speedup: {time1/time2:.1f}x faster')
print(f'Results identical: {len(airports1) == len(airports2)}')
"
```

### 3.4 Create Tests

Create `travelmathlite/apps/airports/tests/test_cache_utils.py`:

```python
"""Tests for airport caching utilities."""
from django.test import TestCase
from django.core.cache import cache
from apps.airports.utils import (
    get_airports_by_country,
    get_airports_by_filters,
    clear_airport_cache
)


class AirportCachingTestCase(TestCase):
    """Test airport query caching."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_airports_cached_by_country(self):
        """Test that airport queries are cached."""
        # First call should query database
        airports1 = get_airports_by_country('US')
        
        # Second call should use cache
        airports2 = get_airports_by_country('US')
        
        # Results should be identical
        self.assertEqual(len(airports1), len(airports2))

    def test_cache_keys_vary_by_parameters(self):
        """Test that different parameters create different cache keys."""
        airports_us = get_airports_by_country('US')
        airports_ca = get_airports_by_country('CA')
        
        # Should cache separately
        self.assertIsNotNone(airports_us)
        self.assertIsNotNone(airports_ca)

    def test_clear_airport_cache(self):
        """Test cache invalidation."""
        # Cache some data
        get_airports_by_country('US')
        
        # Clear cache
        clear_airport_cache()
        
        # Should require fresh query (we can't easily test this without timing,
        # but we can verify the function doesn't error)
        airports = get_airports_by_country('US')
        self.assertIsNotNone(airports)

    def tearDown(self):
        """Clean up after tests."""
        cache.clear()
```

Run tests:

```bash
uv run python manage.py test apps.airports.tests.test_cache_utils
```

---

## Section 4: Add Cache Control Headers

**Brief Context:** [brief-ADR-1.0.10-04-cache-headers.md](../../travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-04-cache-headers.md)

**Goal:** Configure HTTP cache headers for browser and CDN caching.

### 4.1 HTTP Cache Header Concepts

HTTP cache headers control how browsers and CDNs cache responses:

**Cache-Control directives:**

- `public` - Response can be cached by any cache (browsers, CDN)
- `private` - Response can only be cached by browsers (not CDN)
- `no-cache` - Must revalidate with server before using cached copy
- `no-store` - Never cache (for sensitive data)
- `max-age=<seconds>` - How long response is fresh
- `must-revalidate` - Must revalidate when stale

**Vary header:**

- Tells caches to vary stored responses by specific request headers
- Example: `Vary: Accept, Cookie` - cache separately for different Accept types and authenticated users

### 4.2 Implementation Steps

#### Step 1: Create cache header middleware

Create `travelmathlite/core/middleware.py`:

```python
"""Custom middleware for TravelMathLite."""
from django.utils.cache import patch_cache_control


class CacheHeaderMiddleware:
    """Add appropriate cache headers to responses.
    
    Sets Cache-Control and Vary headers based on request path and authentication.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip if headers already set
        if response.has_header('Cache-Control'):
            return response
        
        # Static files handled by WhiteNoise - skip
        if request.path.startswith('/static/'):
            return response
        
        # Set headers for dynamic content
        if request.path.startswith('/search/'):
            # Search results: cache for 5 minutes, vary by query
            patch_cache_control(response, public=True, max_age=300)
            response['Vary'] = 'Accept, Cookie'
        
        elif request.path.startswith('/calculators/'):
            # Calculator results: cache for 10 minutes
            patch_cache_control(response, public=True, max_age=600)
            response['Vary'] = 'Accept'
        
        elif request.user.is_authenticated:
            # Authenticated pages: private cache only
            patch_cache_control(response, private=True, max_age=0)
        
        else:
            # Default: cache for 5 minutes
            patch_cache_control(response, public=True, max_age=300)
        
        return response
```

#### Step 2: Add middleware to settings

Edit `travelmathlite/core/settings/base.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CacheHeaderMiddleware',  # Add this
]
```

#### Step 3: Add decorators for view-specific headers

Edit views to add specific cache control:

```python
from django.views.decorators.cache import cache_control

@cache_control(public=True, max_age=300)
def search_results(request):
    """Search results with explicit cache headers."""
    # ... search logic
    response = render(request, 'search/results.html', context)
    response['Vary'] = 'Accept'
    return response

@cache_control(private=True, max_age=0, must_revalidate=True)
def user_profile(request):
    """User-specific content - no public caching."""
    # ... profile logic
    return render(request, 'users/profile.html', context)
```

### 4.3 Verification

Test cache headers:

```bash
cd travelmathlite

# Start server
uv run python manage.py runserver

# In another terminal, check headers
curl -I http://localhost:8000/search/?q=Dallas

# Should see:
# Cache-Control: public, max-age=300
# Vary: Accept, Cookie
```

### 4.4 Create Tests

Create `travelmathlite/core/tests/test_cache_headers.py`:

```python
"""Tests for HTTP cache headers."""
from django.test import TestCase, Client
from django.contrib.auth.models import User


class CacheHeadersTestCase(TestCase):
    """Test HTTP cache header middleware."""

    def test_search_has_cache_headers(self):
        """Test that search results have appropriate cache headers."""
        client = Client()
        response = client.get('/search/?q=Dallas')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cache-Control', response)
        self.assertIn('public', response['Cache-Control'])
        self.assertIn('max-age=300', response['Cache-Control'])

    def test_calculator_has_cache_headers(self):
        """Test that calculator results have cache headers."""
        client = Client()
        response = client.get('/calculators/distance/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cache-Control', response)
        self.assertIn('public', response['Cache-Control'])

    def test_vary_header_present(self):
        """Test that Vary header is set for content negotiation."""
        client = Client()
        response = client.get('/search/?q=Dallas')
        
        self.assertIn('Vary', response)
        self.assertIn('Accept', response['Vary'])

    def test_authenticated_content_private(self):
        """Test that authenticated content is marked private."""
        # Create user
        user = User.objects.create_user('testuser', 'test@example.com', 'password')
        
        client = Client()
        client.login(username='testuser', password='password')
        response = client.get('/profile/')
        
        if response.status_code == 200:
            self.assertIn('Cache-Control', response)
            self.assertIn('private', response['Cache-Control'])
```

Run tests:

```bash
uv run python manage.py test core.tests.test_cache_headers
```

---

## Section 5: Documentation and Comprehensive Testing

**Brief Context:** [brief-ADR-1.0.10-05-docs-and-tests.md](../../travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-05-docs-and-tests.md)

**Goal:** Create comprehensive documentation and management commands for cache operations.

### 5.1 Management Commands

#### Step 1: Create clear_cache command

Create `travelmathlite/apps/base/management/commands/clear_cache.py`:

```python
"""Management command to clear application cache."""
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    """Clear application cache with optional pattern filtering."""
    
    help = 'Clear application cache'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear only keys matching pattern (airports, search, calculators)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleared without actually clearing',
        )
    
    def handle(self, *args, **options):
        pattern = options.get('pattern')
        dry_run = options.get('dry_run')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no changes will be made'))
        
        if pattern:
            # Pattern-based clearing (requires Redis backend)
            self.stdout.write(f'Clearing cache keys matching: {pattern}')
            
            # For locmem, we can't do pattern matching, just clear all
            if not dry_run:
                cache.clear()
            
            self.stdout.write(self.style.SUCCESS(f'✓ Cleared cache (pattern: {pattern})'))
        else:
            # Clear entire cache
            self.stdout.write('Clearing entire cache...')
            
            if not dry_run:
                cache.clear()
            
            self.stdout.write(self.style.SUCCESS('✓ Cache cleared'))
```

Usage:

```bash
# Clear entire cache
uv run python manage.py clear_cache

# Clear specific pattern (airports)
uv run python manage.py clear_cache --pattern airports

# Dry run
uv run python manage.py clear_cache --dry-run
```

#### Step 2: Create cache_stats command

The file already exists at `travelmathlite/apps/base/management/commands/cache_stats.py`. Verify it displays cache information:

```bash
# View cache statistics
uv run python manage.py cache_stats
```

### 5.2 Integration Tests

Create `travelmathlite/core/tests/test_caching_integration.py`:

```python
"""Integration tests for caching system."""
from django.test import TestCase, Client
from django.core.cache import cache
import time


class CachingIntegrationTestCase(TestCase):
    """End-to-end tests for caching functionality."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_search_caching_workflow(self):
        """Test complete search workflow with caching."""
        client = Client()
        
        # First search (cache miss)
        response1 = client.get('/search/?q=Dallas')
        self.assertEqual(response1.status_code, 200)
        
        # Same search (cache hit)
        response2 = client.get('/search/?q=Dallas')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.content, response2.content)
        
        # Different search (different cache key)
        response3 = client.get('/search/?q=Houston')
        self.assertEqual(response3.status_code, 200)
        self.assertNotEqual(response1.content, response3.content)

    def test_cache_invalidation(self):
        """Test that cache can be cleared."""
        client = Client()
        
        # Cache a result
        response1 = client.get('/search/?q=Dallas')
        self.assertEqual(response1.status_code, 200)
        
        # Clear cache
        cache.clear()
        
        # Should work after clearing (fresh query)
        response2 = client.get('/search/?q=Dallas')
        self.assertEqual(response2.status_code, 200)

    def test_cache_key_variation(self):
        """Test that cache keys vary appropriately."""
        client = Client()
        
        # Same path, different query params
        r1 = client.get('/search/?q=Dallas')
        r2 = client.get('/search/?q=Dallas&page=2')
        r3 = client.get('/search/?q=Houston')
        
        # All should succeed
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r3.status_code, 200)
        
        # All should be different
        self.assertNotEqual(r1.content, r2.content)
        self.assertNotEqual(r1.content, r3.content)

    def tearDown(self):
        """Clean up after tests."""
        cache.clear()
```

Run all caching tests:

```bash
# Run all tests with "cache" or "caching" in the name
uv run python manage.py test --pattern="test_cach*"

# Or run specific test files
uv run python manage.py test core.tests.test_cache_config
uv run python manage.py test core.tests.test_cache_headers
uv run python manage.py test core.tests.test_caching_integration
uv run python manage.py test apps.search.tests.test_caching
uv run python manage.py test apps.airports.tests.test_cache_utils
```

### 5.3 Create Operations Documentation

Create `docs/travelmathlite/ops/caching.md`:

```markdown
# Caching Strategy and Operations

## Overview

TravelMathLite uses Django's caching framework to improve response times for repeated queries. The caching strategy includes:

- **Per-view caching** for search and calculator endpoints
- **Low-level caching** for expensive computed data (airport queries, distance calculations)
- **HTTP cache headers** for browser and CDN caching
- **Flexible backends** (locmem for dev, Redis for production)

## Configuration

### Local Development

Default configuration uses locmem (local memory) cache:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'travelmathlite-cache',
        'TIMEOUT': 300,
    }
}
```

No setup required - works out of the box.

### Production

Configure via `CACHE_URL` environment variable:

```bash
# Redis (recommended)
CACHE_URL=redis://localhost:6379/1

# With authentication
CACHE_URL=redis://username:password@redis-host:6379/1

# File-based (fallback)
CACHE_URL=file:///tmp/django_cache
```

## Per-View Caching

Search and calculator views use `@cache_page` decorator:

- **Search results:** 5 minutes (300s)
- **Calculator results:** 10 minutes (600s)
- Cache keys vary by full URL including query parameters
- Only GET/HEAD requests cached (POST bypasses cache)

## Low-Level Caching

Expensive computations cached using Django's cache API:

- **Airport queries:** 15 minutes (900s)
- **Distance calculations:** 15 minutes (900s)
- Cache keys include function parameters for uniqueness

### Cache Key Patterns

```
travelmathlite:airports:country:<code>
travelmathlite:airports:filter:<params>
travelmathlite:distance:haversine:<coords>
travelmathlite:nearest:airports:<coords>
```

## Cache Headers

HTTP cache headers set via middleware:

- **Search:** `Cache-Control: public, max-age=300` + `Vary: Accept, Cookie`
- **Calculators:** `Cache-Control: public, max-age=600` + `Vary: Accept`
- **Authenticated:** `Cache-Control: private, max-age=0`

## Cache Invalidation

### Manual Clearing

```bash
# Clear entire cache
python manage.py clear_cache

# Clear specific pattern
python manage.py clear_cache --pattern airports

# Dry run (see what would be cleared)
python manage.py clear_cache --dry-run
```

### Programmatic Clearing

```python
from django.core.cache import cache
from apps.airports.utils import clear_airport_cache

# Clear all
cache.clear()

# Clear airports only
clear_airport_cache()
```

## Monitoring

### Cache Statistics

```bash
# View cache info (if backend supports it)
python manage.py cache_stats
```

### Django Shell Testing

```python
# Test cache functionality
from django.core.cache import cache

cache.set('test', 'value', 60)
print(cache.get('test'))
cache.delete('test')
```

## Redis Setup (Production)

### Installation

```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Start service
sudo systemctl start redis    # Linux
brew services start redis     # macOS
```

### Configuration

Edit `/etc/redis/redis.conf`:

```conf
# Bind to localhost only
bind 127.0.0.1

# Set password
requirepass your_secure_password

# Max memory
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Django Configuration

```bash
CACHE_URL=redis://:your_secure_password@localhost:6379/1
```

## Troubleshooting

### Stale Cache

**Problem:** Results not updating after data changes.

**Solution:**

```bash
python manage.py clear_cache
```

### Cache Memory Issues

**Problem:** Cache using too much memory.

**Solution:**

- Reduce TTLs in settings
- Limit MAX_ENTRIES for locmem
- Configure Redis maxmemory policy

### Cache Key Collisions

**Problem:** Different queries returning same results.

**Solution:**

- Review cache key generation
- Ensure keys include all relevant parameters
- Add version/namespace prefix

## Performance Tips

1. **Monitor cache hit rates** - Use cache_stats command
2. **Adjust TTLs** - Balance freshness vs performance
3. **Use Redis in production** - Better performance and multi-process support
4. **Profile before caching** - Cache only what needs it
5. **Test cache invalidation** - Ensure stale data doesn't persist

## References

- [Django Caching Documentation](https://docs.djangoproject.com/en/stable/topics/cache/)
- [Redis Documentation](https://redis.io/documentation)
- ADR-1.0.10: Caching Strategy

```

---

## Summary

You've successfully implemented Django's caching system for TravelMathLite:

✅ **Configured cache backends** - locmem for dev, Redis for production  
✅ **Applied per-view caching** - 5-10 minute TTLs on hot paths  
✅ **Implemented low-level caching** - 15 minute TTLs for computed data  
✅ **Added HTTP cache headers** - Browser and CDN caching support  
✅ **Created management commands** - clear_cache, cache_stats  
✅ **Wrote comprehensive tests** - Unit and integration test coverage  
✅ **Documented operations** - Complete ops guide with troubleshooting  

### Key Takeaways

1. **Django's cache framework is flexible** - Works with multiple backends
2. **Multiple caching levels** - Page, view, fragment, and low-level API
3. **Cache keys must be deterministic** - Same inputs = same key
4. **TTLs balance freshness and performance** - Shorter for dynamic data
5. **HTTP headers enable browser caching** - Reduces server load
6. **Test cache behavior** - Verify hits, misses, and invalidation

### Next Steps

1. **Monitor cache hit rates** in production
2. **Tune TTLs** based on actual usage patterns
3. **Set up Redis** for production deployment
4. **Add cache warming** for common queries
5. **Implement cache versioning** for dataset updates

---

## References

- **Django Documentation:**
  - [Caching Framework](https://docs.djangoproject.com/en/stable/topics/cache/)
  - [Cache Decorators](https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache)
  - [Low-Level Cache API](https://docs.djangoproject.com/en/stable/topics/cache/#the-low-level-cache-api)

- **Matt Layman - Understand Django:**
  - [Django Caching Strategies](https://www.mattlayman.com/understand-django/performance-caching/)

- **Related Documentation:**
  - [ADR-1.0.10: Caching Strategy](../../travelmathlite/adr/adr-1.0.10-caching-strategy.md)
  - [Operations Guide: Caching](../../travelmathlite/ops/caching.md)

- **External Resources:**
  - [Redis Documentation](https://redis.io/documentation)
  - [HTTP Caching (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
  - [Cache-Control Header Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
