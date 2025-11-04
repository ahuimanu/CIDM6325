"""Django management command to export airports to fixture JSON."""

import logging
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.core.serializers import serialize

from apps.airports.models import Airport

logger = logging.getLogger(__name__)

DEFAULT_FIXTURE_PATH = "apps/airports/fixtures/airports.json"


class Command(BaseCommand):
    """Export airports to JSON fixture for rehydration."""

    help = "Export airports to JSON fixture"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "--output",
            type=str,
            default=DEFAULT_FIXTURE_PATH,
            help=f"Output fixture path (default: {DEFAULT_FIXTURE_PATH})",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit number of airports to export (for testing)",
        )
        parser.add_argument(
            "--filter-iata",
            action="store_true",
            help="Only export airports with IATA codes",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the export command."""
        output_path = options["output"]
        limit = options.get("limit")
        filter_iata = options["filter_iata"]

        self.stdout.write(self.style.SUCCESS("Starting airport export..."))

        # Build queryset
        queryset = Airport.objects.all()

        if filter_iata:
            queryset = queryset.exclude(iata_code="")
            self.stdout.write("Filtering to airports with IATA codes")

        if limit:
            queryset = queryset[:limit]
            self.stdout.write(f"Limiting to {limit} airports")

        count = queryset.count()
        self.stdout.write(f"Exporting {count} airports...")

        # Serialize to JSON
        data = serialize("json", queryset, indent=2)

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(data)

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} airports to {output_path}"))
        self.stdout.write(f"\nTo load this fixture: uv run python manage.py loaddata {output_path}")
