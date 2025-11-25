# BRIEF: Configure cache backend

Goal

- Configure Django `CACHES` setting with locmem for local development and optional Redis/file-based backend for production via environment variable, addressing PRD §4 F-013 and §7 NF-001.

Scope (single PR)

- Files to touch:
  - `travelmathlite/core/settings/base.py` — Add `CACHES` configuration
  - `travelmathlite/core/settings/local.py` — Ensure locmem is default
  - `travelmathlite/core/settings/prod.py` — Support `CACHE_URL` environment variable
  - `travelmathlite/.env.example` — Document `CACHE_URL` variable
  - `travelmathlite/core/tests/test_cache_config.py` — Tests for cache configuration
- Non-goals: Implementing actual cache decorators (covered in brief-02)

Standards

- Commits: conventional style (feat: configure cache backend).
- No secrets; use environment variables for production Redis URLs.
- Django tests: use unittest/Django TestCase (no pytest).
- Follow django-environ pattern for `CACHE_URL` parsing.

Acceptance

- Cache backend: locmem in local, configurable in prod via `CACHE_URL`
- Default TTL: 300 seconds (5 minutes)
- Environment variable documented in `.env.example`
- Tests verify cache configuration loads correctly in both environments
- Include migration? no
- Update docs: `docs/travelmathlite/ops/caching.md` (create if needed)

Prompts for Copilot

- "Configure Django CACHES setting in core/settings/base.py using locmem as default, with support for CACHE_URL environment variable in prod.py. Parse cache URLs using django-environ's cache_url() method. Default TTL should be 300 seconds."
- "Create tests in core/tests/test_cache_config.py that verify cache backend is correctly configured for local (locmem) and production (from CACHE_URL environment variable)."
- "Add CACHE_URL to .env.example with Redis example URL and locmem example."
- "Document cache configuration in docs/travelmathlite/ops/caching.md including backend options, environment variables, and TTL configuration."

Trace

- FR-F-013-1: Enable per-view/low-level caching on hot paths
- NF-001: Performance p95 targets

Implementation notes

- Use `django.core.cache.backends.locmem.LocMemCache` for local
- Support `redis://` and `file://` URLs in production via `CACHE_URL`
- Set `KEY_PREFIX` to `travelmathlite:` for Redis namespace isolation
- Configure `OPTIONS` with `MAX_ENTRIES` for locmem (e.g., 1000)

Verification

```bash
# Local (should use locmem)
cd travelmathlite
uv run python manage.py shell -c "
from django.core.cache import cache
print(f'Backend: {cache.__class__.__name__}')
cache.set('test_key', 'test_value', 60)
print(f'Cached value: {cache.get(\"test_key\")}')
"

# Production with Redis (requires CACHE_URL)
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  CACHE_URL=redis://localhost:6379/1 \
  uv run python manage.py shell -c "
from django.core.cache import cache
print(f'Backend: {cache.__class__.__name__}')
"

# Run tests
uv run python manage.py test core.tests.test_cache_config
```

Expected cache configuration structure

```python
# base.py
CACHES = {
    'default': env.cache_url('CACHE_URL', default='locmem://'),
}

# Alternative explicit configuration:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'travelmathlite-cache',
        'TIMEOUT': 300,  # 5 minutes default
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    }
}
```

Example CACHE_URL formats

```bash
# Local memory (default)
CACHE_URL=locmem://

# File-based cache
CACHE_URL=file:///tmp/django_cache

# Redis
CACHE_URL=redis://localhost:6379/1
CACHE_URL=redis://username:password@redis-host:6379/1

# Memcached
CACHE_URL=memcached://127.0.0.1:11211
```
