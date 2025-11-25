"""Django management command to update airport data from OurAirports dataset.

This command can be scheduled (e.g., via cron) to periodically refresh airport data.
"""

import logging
from datetime import datetime
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from apps.airports.models import Airport

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Update airport data from OurAirports dataset."""

    help = "Update airport data by re-importing from OurAirports (idempotent)"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "--url",
            type=str,
            help="Override default CSV URL",
        )
        parser.add_argument(
            "--filter-iata",
            action="store_true",
            help="Only import airports with IATA codes",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be updated without making changes",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update even if recently updated",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the update command."""
        dry_run = options["dry_run"]
        filter_iata = options["filter_iata"]
        url = options.get("url")

        start_time = datetime.now()

        self.stdout.write("=" * 60)
        self.stdout.write("Airport Data Update")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write("")

        # Get current counts
        initial_count = Airport.objects.count()
        self.stdout.write(f"Current airports in database: {initial_count}")
        self.stdout.write("")

        if dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE] No changes will be saved"))
            self.stdout.write("")

        # Build import command arguments
        import_kwargs: dict[str, Any] = {
            "stdout": self.stdout,
            "stderr": self.stderr,
        }

        if url:
            import_kwargs["url"] = url

        if filter_iata:
            import_kwargs["filter_iata"] = True

        if dry_run:
            import_kwargs["dry_run"] = True

        # Run import command
        final_count = initial_count
        net_change = 0

        try:
            self.stdout.write("Fetching latest data from OurAirports...")
            self.stdout.write("")

            with transaction.atomic():
                call_command("import_airports", **import_kwargs)

                if dry_run:
                    # Rollback transaction in dry-run mode
                    transaction.set_rollback(True)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Update failed: {e}"))
            # Log a concise error without a traceback to avoid noisy test output
            logger.error("Airport data update failed: %s", e)
            return

        # Get updated counts
        if not dry_run:
            final_count = Airport.objects.count()
            net_change = final_count - initial_count

            self.stdout.write("")
            self.stdout.write("=" * 60)
            self.stdout.write("Update Summary")
            self.stdout.write("=" * 60)
            self.stdout.write(f"Initial count: {initial_count}")
            self.stdout.write(f"Final count: {final_count}")
            self.stdout.write(f"Net change: {net_change:+d}")
        else:
            self.stdout.write("")
            self.stdout.write("=" * 60)
            self.stdout.write("[DRY RUN] No changes were saved")
            self.stdout.write("=" * 60)

        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        self.stdout.write("")
        self.stdout.write(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"Duration: {duration:.2f} seconds")
        self.stdout.write("")

        if not dry_run:
            self.stdout.write(self.style.SUCCESS("✓ Airport data updated successfully!"))
            logger.info(f"Airport data updated: {initial_count} → {final_count} (net: {net_change:+d}) in {duration:.2f}s")
        else:
            self.stdout.write(self.style.SUCCESS("✓ Dry run completed"))
