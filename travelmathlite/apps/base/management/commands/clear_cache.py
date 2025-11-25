"""Management command to clear application cache.

Usage:
    python manage.py clear_cache              # Clear entire cache
    python manage.py clear_cache --pattern airports    # Clear airport cache only
    python manage.py clear_cache --pattern search      # Clear search cache only
    python manage.py clear_cache --pattern calculators # Clear calculator cache only
"""

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Clear application cache with optional pattern filtering."""

    help = "Clear application cache (entire cache or pattern-based)"

    def add_arguments(self, parser) -> None:
        """Add command arguments.

        Args:
            parser: Argument parser to configure.
        """
        parser.add_argument(
            "--pattern",
            type=str,
            help="Clear only keys matching pattern (airports, search, calculators)",
        )

    def handle(self, *args, **options) -> None:  # type: ignore[no-untyped-def]
        """Execute the command.

        Args:
            *args: Positional arguments.
            **options: Keyword arguments including 'pattern'.
        """
        pattern = options.get("pattern")

        if pattern:
            # Pattern-based clearing (requires Redis backend)
            try:
                # Try Redis-specific pattern deletion
                if hasattr(cache, "delete_pattern"):
                    deleted = cache.delete_pattern(f"travelmathlite:{pattern}:*")  # type: ignore[attr-defined]
                    self.stdout.write(self.style.SUCCESS(f"✓ Cleared {deleted} cache keys for pattern: {pattern}"))
                else:
                    # Fallback: clear entire cache if pattern deletion not supported
                    self.stdout.write(self.style.WARNING("Pattern deletion not supported by cache backend (requires Redis)"))
                    self.stdout.write("Clearing entire cache instead...")
                    cache.clear()
                    self.stdout.write(self.style.SUCCESS("✓ Cache cleared"))
            except Exception as e:
                raise CommandError(f"Failed to clear cache: {e}") from e
        else:
            # Clear entire cache
            cache.clear()
            self.stdout.write(self.style.SUCCESS("✓ Entire cache cleared"))
