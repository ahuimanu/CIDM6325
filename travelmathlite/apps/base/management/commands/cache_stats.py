"""Management command to display cache statistics.

Usage:
    python manage.py cache_stats    # Display cache backend info and statistics

For Redis backends, shows:
- Hit rate
- Memory usage
- Keyspace info

For other backends, shows:
- Backend type only
"""

from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Display cache statistics and backend information."""

    help = "Display cache statistics (backend-specific)"

    def handle(self, *args, **options) -> None:  # type: ignore[no-untyped-def]
        """Execute the command.

        Args:
            *args: Positional arguments.
            **options: Keyword arguments.
        """
        backend = cache.__class__.__name__
        self.stdout.write(self.style.SUCCESS(f"Cache Backend: {backend}"))

        # Check for Redis-like backend
        if "Redis" in backend:
            try:
                # Try to access Redis client (different methods for different backends)
                client = None

                # Try to get the underlying client for django.core.cache.backends.redis.RedisCache
                if hasattr(cache, "get_master_client"):
                    client = cache.get_master_client()  # type: ignore[attr-defined]
                elif hasattr(cache, "client"):
                    client = cache.client  # type: ignore[attr-defined]

                if client and hasattr(client, "info"):
                    # Stats info
                    info = client.info("stats")

                    self.stdout.write(self.style.SUCCESS("\nRedis Statistics:"))
                    hits = info.get("keyspace_hits", 0)
                    misses = info.get("keyspace_misses", 0)
                    total = hits + misses

                    self.stdout.write(f"  Hits: {hits:,}")
                    self.stdout.write(f"  Misses: {misses:,}")

                    if total > 0:
                        hit_rate = (hits / total) * 100
                        self.stdout.write(self.style.SUCCESS(f"  Hit Rate: {hit_rate:.2f}%"))
                    else:
                        self.stdout.write("  Hit Rate: N/A (no requests yet)")

                    # Memory info
                    memory_info = client.info("memory")
                    used_memory = memory_info.get("used_memory_human", "N/A")
                    max_memory = memory_info.get("maxmemory_human", "unlimited")
                    self.stdout.write(f"  Memory Used: {used_memory}")
                    self.stdout.write(f"  Max Memory: {max_memory}")

                    # Keyspace info
                    keyspace_info = client.info("keyspace")
                    if keyspace_info:
                        self.stdout.write(self.style.SUCCESS("\nKeyspace Info:"))
                        for db, info_str in keyspace_info.items():
                            self.stdout.write(f"  {db}: {info_str}")
                    else:
                        self.stdout.write("\nKeyspace: empty")
                else:
                    self.stdout.write(self.style.WARNING("\nRedis-like backend detected but cannot access client"))
                    self.stdout.write("Statistics not available")

            except ImportError:
                self.stdout.write(self.style.WARNING("\nRedis backend detected but redis-py not installed"))
                self.stdout.write("Install: pip install redis")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"\nCould not fetch Redis stats: {e}"))
        else:
            self.stdout.write(self.style.WARNING("\nStatistics not available for this cache backend"))
            self.stdout.write("Use Redis backend for detailed statistics")
            self.stdout.write("\nConfiguration:")
            self.stdout.write("  CACHE_BACKEND=django.core.cache.backends.redis.RedisCache")
            self.stdout.write("  CACHE_LOCATION=redis://localhost:6379/1")
