# BRIEF: Documentation and comprehensive testing

Goal

- Create comprehensive caching documentation and integration tests that verify cache behavior, performance improvements, and invalidation strategies, addressing PRD §4 F-013 and §7 NF-001.

Scope (single PR)

- Files to touch:
  - `docs/travelmathlite/ops/caching.md` — Comprehensive caching operations guide
  - `travelmathlite/core/tests/test_caching_integration.py` — Integration tests
  - `travelmathlite/management/commands/clear_cache.py` — Management command for cache clearing
  - `travelmathlite/management/commands/cache_stats.py` — Management command for cache statistics
  - `README.md` — Update with caching configuration instructions
- Non-goals: Performance benchmarking suite (future work)

Standards

- Commits: conventional style (docs: add caching documentation and tests).
- Documentation should cover: configuration, usage patterns, invalidation, monitoring.
- Django tests: use unittest/Django TestCase (no pytest).
- Include examples for Redis setup and troubleshooting.

Acceptance

- Operations guide covers: backend config, per-view caching, low-level caching, headers, monitoring, troubleshooting
- Management commands for cache clearing and stats
- Integration tests verify end-to-end cache behavior
- Tests verify cache hit rate and performance improvement
- Documentation includes Redis setup for production
- Include migration? no
- All previous brief tests passing

Prompts for Copilot

- "Create comprehensive caching documentation in docs/travelmathlite/ops/caching.md covering: cache backend configuration, per-view caching with @cache_page, low-level caching patterns, cache headers, invalidation strategies, Redis setup, monitoring, and troubleshooting."
- "Create management command clear_cache.py that clears all application caches with options to target specific cache patterns (airports, search, calculators)."
- "Create management command cache_stats.py that displays cache statistics if backend supports it (Redis info, hit rate, memory usage)."
- "Create integration tests in test_caching_integration.py that verify complete cache workflows: search with caching, cache invalidation, performance improvements, cache key variation."

Trace

- FR-F-013-1: Enable per-view/low-level caching on hot paths
- NF-001: Performance p95 targets
- INV-1: Cache TTLs respected; content varies by query params

Implementation notes

- Documentation structure:
  - Overview and architecture
  - Configuration (local vs prod)
  - Per-view caching usage
  - Low-level caching patterns
  - Cache headers
  - Invalidation strategies
  - Monitoring and debugging
  - Redis setup guide
  - Troubleshooting
- Management commands should be in `apps/base/management/commands/`
- Integration tests should cover realistic user workflows

Verification

```bash
cd travelmathlite

# Clear cache via management command
uv run python manage.py clear_cache
uv run python manage.py clear_cache --pattern airports
uv run python manage.py clear_cache --pattern search

# View cache statistics (if Redis)
uv run python manage.py cache_stats

# Run all caching tests
uv run python manage.py test core.tests.test_cache_config
uv run python manage.py test core.tests.test_cache_headers
uv run python manage.py test core.tests.test_caching_integration
uv run python manage.py test apps.search.tests.test_caching
uv run python manage.py test apps.calculators.tests.test_caching
uv run python manage.py test apps.airports.tests.test_cache_utils

# Verify all tests pass
uv run python manage.py test --pattern="test_cach*"
```

Documentation structure (caching.md)

```markdown
# Caching Strategy and Operations

## Overview
- Architecture diagram
- Cache backend choices
- TTL strategy

## Configuration

### Local Development
- locmem backend (default)
- No setup required

### Production
- Redis backend (recommended)
- File-based fallback
- Environment variables

## Per-View Caching

### Usage
- @cache_page decorator
- TTL settings
- Query parameter variation

### Examples
- Search results (5 min)
- Calculator results (10 min)

## Low-Level Caching

### Usage
- django.core.cache API
- Cache key patterns
- get_or_set pattern

### Examples
- Airport queries
- Distance calculations
- Computed lists

## Cache Headers

### Browser Caching
- Cache-Control directives
- Vary headers
- ETag support

### CDN Considerations
- Public vs private
- s-maxage directive

## Cache Invalidation

### Strategies
- Time-based (TTL)
- Manual invalidation
- Dataset version keys

### Tools
- clear_cache command
- Invalidation helpers

## Monitoring

### Cache Statistics
- Hit rate
- Memory usage
- Key patterns

### Debugging
- Cache inspection
- Key listing
- Performance profiling

## Redis Setup

### Installation
### Configuration
### Security
### Monitoring

## Troubleshooting

### Common Issues
- Stale cache
- Memory limits
- Key conflicts

### Solutions
- Clear cache
- Adjust TTLs
- Check configuration
```

Management command: clear_cache.py

```python
# apps/base/management/commands/clear_cache.py
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear application cache'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear only keys matching pattern (airports, search, calculators)',
        )
    
    def handle(self, *args, **options):
        pattern = options.get('pattern')
        
        if pattern:
            # Pattern-based clearing (requires Redis)
            try:
                cache.delete_pattern(f"travelmathlite:{pattern}:*")
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Cleared cache for pattern: {pattern}')
                )
            except AttributeError:
                self.stdout.write(
                    self.style.WARNING('Pattern deletion not supported by cache backend')
                )
                self.stdout.write('Clearing entire cache instead...')
                cache.clear()
        else:
            # Clear entire cache
            cache.clear()
            self.stdout.write(self.style.SUCCESS('✓ Cache cleared'))
```

Management command: cache_stats.py

```python
# apps/base/management/commands/cache_stats.py
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Display cache statistics'
    
    def handle(self, *args, **options):
        backend = cache.__class__.__name__
        self.stdout.write(f'Cache Backend: {backend}')
        
        # Try to get backend-specific stats
        if hasattr(cache, '_cache'):  # Redis
            try:
                import redis
                info = cache._cache.get_client().info('stats')
                
                self.stdout.write('\nRedis Statistics:')
                self.stdout.write(f"  Hits: {info.get('keyspace_hits', 0)}")
                self.stdout.write(f"  Misses: {info.get('keyspace_misses', 0)}")
                
                hits = info.get('keyspace_hits', 0)
                misses = info.get('keyspace_misses', 0)
                total = hits + misses
                if total > 0:
                    hit_rate = (hits / total) * 100
                    self.stdout.write(f"  Hit Rate: {hit_rate:.2f}%")
                
                # Memory info
                memory_info = cache._cache.get_client().info('memory')
                used_memory = memory_info.get('used_memory_human', 'N/A')
                self.stdout.write(f"  Memory Used: {used_memory}")
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not fetch Redis stats: {e}'))
        else:
            self.stdout.write('\nStatistics not available for this cache backend')
```

Integration test structure

```python
# core/tests/test_caching_integration.py
from django.test import TestCase, Client
from django.core.cache import cache
import time

class CachingIntegrationTestCase(TestCase):
    fixtures = ['airports.json']
    
    def setUp(self):
        cache.clear()
    
    def test_search_workflow_with_caching(self):
        """Test complete search workflow with caching."""
        client = Client()
        
        # First search - cache miss
        start = time.time()
        response1 = client.get('/search/?q=Dallas')
        time1 = time.time() - start
        
        self.assertEqual(response1.status_code, 200)
        
        # Repeat search - cache hit
        start = time.time()
        response2 = client.get('/search/?q=Dallas')
        time2 = time.time() - start
        
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.content, response2.content)
        
        # Second request should be faster
        self.assertLess(time2, time1)
    
    def test_cache_invalidation_workflow(self):
        """Test cache clearing and re-population."""
        client = Client()
        
        # Populate cache
        response1 = client.get('/search/?q=Dallas')
        self.assertEqual(response1.status_code, 200)
        
        # Clear cache
        cache.clear()
        
        # Next request should be cache miss
        response2 = client.get('/search/?q=Dallas')
        self.assertEqual(response2.status_code, 200)
    
    def test_cache_key_variation(self):
        """Test that different queries use different cache keys."""
        client = Client()
        
        # Different searches should return different results
        dallas = client.get('/search/?q=Dallas')
        houston = client.get('/search/?q=Houston')
        
        self.assertNotEqual(dallas.content, houston.content)
    
    def test_cache_respects_ttl(self):
        """Test that cache entries expire after TTL."""
        # This test would need to wait for TTL to expire
        # or use a mock/patch to simulate time passing
        pass
```

Test checklist

- [ ] Cache backend configuration tests pass
- [ ] Per-view caching tests pass
- [ ] Low-level caching tests pass
- [ ] Cache headers tests pass
- [ ] Integration tests pass
- [ ] Management commands work
- [ ] Documentation is complete
- [ ] All edge cases covered (TTL expiry, key conflicts, etc.)
