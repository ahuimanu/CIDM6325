# BRIEF: Add cache control headers

Goal

- Configure appropriate HTTP cache headers (`Cache-Control`, `ETag`, `Vary`) for static assets and API responses to enable browser/CDN caching, addressing PRD §7 NF-001.

Scope (single PR)

- Files to touch:
  - `travelmathlite/core/middleware.py` — Create cache header middleware
  - `travelmathlite/core/settings/base.py` — Add middleware to MIDDLEWARE list
  - `travelmathlite/apps/search/views.py` — Add conditional `Cache-Control` headers
  - `travelmathlite/apps/calculators/views.py` — Add conditional headers
  - `travelmathlite/core/tests/test_cache_headers.py` — Tests for header behavior
- Non-goals: CDN configuration (out of scope per ADR)

Standards

- Commits: conventional style (feat: add cache control headers).
- Use Django's `@cache_control` decorator for view-specific headers.
- Django tests: use unittest/Django TestCase (no pytest).
- Document header strategy in code and ops docs.

Acceptance

- Static assets: `Cache-Control: public, max-age=31536000` (1 year)
- Dynamic content: `Cache-Control: private, max-age=300` (5 minutes)
- API responses: Include `Vary: Accept` header
- Search results: Include `Vary: Cookie` for authenticated users
- Tests verify headers are present and correct
- Include migration? no
- Update docs: add cache headers section to `docs/travelmathlite/ops/caching.md`

Prompts for Copilot

- "Create cache header middleware in core/middleware.py that sets appropriate Cache-Control headers based on response type. Static assets should have max-age=31536000, dynamic content max-age=300."
- "Add @cache_control decorator to search and calculator views to set appropriate cache headers. Use cache_control(public=True, max_age=300) for public content."
- "Create tests in core/tests/test_cache_headers.py that verify Cache-Control, Vary, and ETag headers are present and correct for different response types."
- "Document cache header strategy in docs/travelmathlite/ops/caching.md including browser caching, CDN considerations, and header values."

Trace

- FR-F-013-1: Enable per-view/low-level caching on hot paths
- NF-001: Performance p95 targets

Implementation notes

- Import: `from django.views.decorators.cache import cache_control`
- Middleware: `django.middleware.cache.UpdateCacheMiddleware` and `FetchFromCacheMiddleware`
- Headers to set:
  - `Cache-Control: public` (cacheable by browsers/CDN)
  - `Cache-Control: private` (cacheable by browser only)
  - `Cache-Control: no-cache` (revalidate every time)
  - `Cache-Control: no-store` (never cache - for sensitive data)
  - `Vary: Accept, Cookie` (vary cache by these headers)
  - `ETag` (entity tag for conditional requests)

Verification

```bash
cd travelmathlite

# Test cache headers on static files
curl -I http://localhost:8000/static/css/style.css

# Test cache headers on search results
curl -I http://localhost:8000/search/?q=Dallas

# Test cache headers on calculator
curl -I http://localhost:8000/calculators/distance/

# Run tests
uv run python manage.py test core.tests.test_cache_headers
```

Example middleware implementation

```python
# core/middleware.py
from django.utils.cache import patch_response_headers, patch_cache_control

class CacheHeaderMiddleware:
    """Add appropriate cache headers to responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip if headers already set
        if response.has_header('Cache-Control'):
            return response
        
        # Static files already handled by WhiteNoise
        # Set headers for dynamic content
        if request.path.startswith('/search/'):
            # Search results: cache for 5 minutes, vary by query
            patch_cache_control(response, public=True, max_age=300)
            response['Vary'] = 'Accept, Cookie'
        elif request.path.startswith('/calculators/'):
            # Calculator results: cache for 10 minutes
            patch_cache_control(response, public=True, max_age=600)
        elif request.user.is_authenticated:
            # Authenticated pages: private cache only
            patch_cache_control(response, private=True, max_age=0)
        else:
            # Default: cache for 5 minutes
            patch_cache_control(response, public=True, max_age=300)
        
        return response
```

Example decorator usage

```python
# apps/search/views.py
from django.views.decorators.cache import cache_control

@cache_control(public=True, max_age=300)
def search_results(request):
    """Search results cached for 5 minutes."""
    query = request.GET.get('q', '')
    # ... search logic
    response = render(request, 'search/results.html', context)
    response['Vary'] = 'Accept'
    return response

@cache_control(private=True, max_age=0, must_revalidate=True)
def user_search_history(request):
    """User-specific content - no public caching."""
    # ... user-specific logic
    return render(request, 'search/history.html', context)
```

Test structure

```python
# core/tests/test_cache_headers.py
from django.test import TestCase, Client

class CacheHeadersTestCase(TestCase):
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
    
    def test_vary_header_present(self):
        """Test that Vary header is set for content negotiation."""
        client = Client()
        response = client.get('/search/?q=Dallas')
        
        self.assertIn('Vary', response)
        self.assertIn('Accept', response['Vary'])
    
    def test_authenticated_content_private(self):
        """Test that authenticated content is marked private."""
        # Create and login user
        from django.contrib.auth.models import User
        user = User.objects.create_user('test', 'test@example.com', 'password')
        
        client = Client()
        client.login(username='test', password='password')
        response = client.get('/profile/')
        
        self.assertIn('Cache-Control', response)
        self.assertIn('private', response['Cache-Control'])
```

Cache-Control directives reference

```
public              - Cacheable by any cache (browsers, CDN)
private             - Cacheable by browser only (not CDN)
no-cache            - Must revalidate before use
no-store            - Never cache (sensitive data)
max-age=<seconds>   - Cache lifetime
must-revalidate     - Must revalidate when stale
s-maxage=<seconds>  - CDN cache lifetime (overrides max-age)
```

Vary header usage

```
Vary: Accept        - Cache varies by Accept header (API responses)
Vary: Cookie        - Cache varies by cookies (authenticated content)
Vary: Accept-Encoding  - Cache varies by encoding (gzip, etc.)
Vary: *             - Do not cache (varies by everything)
```

Header strategies by content type

- **Static assets**: `public, max-age=31536000, immutable` (handled by WhiteNoise)
- **Public API**: `public, max-age=300, Vary: Accept`
- **Search results**: `public, max-age=300, Vary: Cookie`
- **User content**: `private, max-age=0, must-revalidate`
- **Sensitive data**: `no-store, no-cache, must-revalidate`
