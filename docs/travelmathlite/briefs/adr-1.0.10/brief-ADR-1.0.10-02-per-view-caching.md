# BRIEF: Implement per-view caching with decorators

Goal

- Apply Django's `@cache_page` decorator to hot-path views (search results, nearest airport) with short TTLs (5-15 minutes), addressing PRD §4 F-013 and §7 NF-001.

Scope (single PR)

- Files to touch:
  - `travelmathlite/apps/search/views.py` — Add `@cache_page` to search views
  - `travelmathlite/apps/calculators/views.py` — Add `@cache_page` to nearest airport view
  - `travelmathlite/apps/search/tests/test_caching.py` — Tests for cache behavior
  - `travelmathlite/apps/calculators/tests/test_caching.py` — Tests for cache behavior
- Non-goals: Low-level caching (covered in brief-03), CDN layer

Standards

- Commits: conventional style (feat: add per-view caching to search/calculators).
- Cache keys must vary by query parameters (use `cache_page` with `key_prefix`).
- Django tests: use unittest/Django TestCase (no pytest).
- Respect CSRF tokens and POST requests (cache GET only).

Acceptance

- Search results cached for 5 minutes
- Nearest airport results cached for 10 minutes
- Cache keys vary by query string
- POST requests bypass cache
- Tests verify cache hits/misses
- Include migration? no
- Update docs: add cache behavior to `docs/travelmathlite/ops/caching.md`

Prompts for Copilot

- "Add @cache_page decorator to search views in apps/search/views.py with 300 second (5 minute) TTL. Ensure cache keys vary by query parameters."
- "Add @cache_page decorator to nearest airport calculator view with 600 second (10 minute) TTL. Preserve existing functionality and ensure GET requests are cached but POST requests bypass cache."
- "Create tests in apps/search/tests/test_caching.py that verify repeated identical search queries return cached results (faster response, cache hit markers in logs)."
- "Create tests in apps/calculators/tests/test_caching.py that verify nearest airport queries are cached with proper key variation by parameters."

Trace

- FR-F-013-1: Enable per-view/low-level caching on hot paths
- NF-001: Performance p95 targets
- INV-1: Cache TTLs respected; content varies by query params

Implementation notes

- Import: `from django.views.decorators.cache import cache_page`
- Usage: `@cache_page(300)` for function-based views
- For class-based views: `method_decorator(cache_page(300), name='dispatch')`
- Cache varies by: full URL including query string (default behavior)
- Ensure CSRF protection still works (cache_page preserves this)

Verification

```bash
cd travelmathlite

# Test search view caching
uv run python manage.py shell -c "
from django.test import Client
import time

client = Client()

# First request (cache miss)
start = time.time()
response1 = client.get('/search/?q=Dallas')
time1 = time.time() - start

# Second request (cache hit)
start = time.time()
response2 = client.get('/search/?q=Dallas')
time2 = time.time() - start

print(f'First request: {time1:.4f}s')
print(f'Second request: {time2:.4f}s')
print(f'Speedup: {time1/time2:.2f}x')
"

# Run caching tests
uv run python manage.py test apps.search.tests.test_caching
uv run python manage.py test apps.calculators.tests.test_caching
```

Example decorator usage

```python
# Function-based view
from django.views.decorators.cache import cache_page

@cache_page(300)  # 5 minutes
def search_results(request):
    query = request.GET.get('q', '')
    # ... search logic
    return render(request, 'search/results.html', context)

# Class-based view
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View

@method_decorator(cache_page(600), name='dispatch')  # 10 minutes
class NearestAirportView(View):
    def get(self, request):
        # ... calculator logic
        return render(request, 'calculators/nearest.html', context)
```

Test structure

```python
from django.test import TestCase, Client
from django.core.cache import cache

class SearchCachingTestCase(TestCase):
    def setUp(self):
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
        
        # Should not be identical (different results)
        self.assertNotEqual(response1.content, response2.content)
```

Cache key variation patterns

- `/search/?q=Dallas` — Cached separately
- `/search/?q=Houston` — Cached separately
- `/search/?q=Dallas&page=2` — Cached separately (varies by all params)
- POST requests — Never cached (only GET/HEAD)
