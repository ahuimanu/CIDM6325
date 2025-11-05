"""Django management command to import airports from OurAirports CSV."""

import csv
import logging
import ssl
from typing import Any
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandParser

from apps.airports.models import Airport

logger = logging.getLogger(__name__)

OURAIRPORTS_CSV_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
DEFAULT_LOCAL_PATH = "downloads/airports.csv"


class Command(BaseCommand):
    """Import airports from OurAirports CSV dataset."""

    help = "Import airports from OurAirports CSV (idempotent)"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "--url",
            type=str,
            default=OURAIRPORTS_CSV_URL,
            help=f"CSV URL to fetch (default: {OURAIRPORTS_CSV_URL})",
        )
        parser.add_argument(
            "--file",
            type=str,
            help="Local CSV file path (overrides --url)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and validate without saving to database",
        )
        parser.add_argument(
            "--filter-iata",
            action="store_true",
            help="Only import airports with IATA codes",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit number of airports to import (for testing)",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the import command."""
        dry_run = options["dry_run"]
        filter_iata = options["filter_iata"]
        limit = options.get("limit")
        local_file = options.get("file")
        url = options["url"]

        self.stdout.write(self.style.SUCCESS("Starting airport import..."))

        # Determine CSV source
        if local_file:
            csv_path = local_file
            self.stdout.write(f"Using local file: {csv_path}")
        else:
            csv_path = DEFAULT_LOCAL_PATH
            self.stdout.write(f"Downloading from: {url}")
            try:
                # Create SSL context that doesn't verify certificates (for development)
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                # Download with SSL context
                with urlopen(url, context=ssl_context) as response:
                    with open(csv_path, "wb") as out_file:
                        out_file.write(response.read())
                self.stdout.write(self.style.SUCCESS(f"Downloaded to {csv_path}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to download CSV: {e}"))
                return

        # Parse and import
        stats = {
            "total": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
        }

        try:
            with open(csv_path, encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    stats["total"] += 1

                    # Check limit
                    if limit and stats["total"] > limit:
                        break

                    # Filter by IATA if requested
                    if filter_iata and not row.get("iata_code"):
                        stats["skipped"] += 1
                        continue

                    # Validate required fields
                    try:
                        self._validate_row(row)
                    except ValueError as e:
                        logger.warning(f"Skipping row {stats['total']}: {e}")
                        stats["errors"] += 1
                        continue

                    # Process row
                    if dry_run:
                        self.stdout.write(
                            f"[DRY RUN] Would process: {row.get('name')} "
                            f"({row.get('iata_code') or row.get('ident')})"
                        )
                    else:
                        created = self._upsert_airport(row)
                        if created:
                            stats["created"] += 1
                        else:
                            stats["updated"] += 1

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Import failed: {e}"))
            return

        # Report stats
        self.stdout.write(self.style.SUCCESS("\n=== Import Summary ==="))
        self.stdout.write(f"Total rows: {stats['total']}")
        self.stdout.write(f"Created: {stats['created']}")
        self.stdout.write(f"Updated: {stats['updated']}")
        self.stdout.write(f"Skipped: {stats['skipped']}")
        self.stdout.write(f"Errors: {stats['errors']}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY RUN] No changes saved to database"))
        else:
            self.stdout.write(self.style.SUCCESS("\nImport complete!"))

    def _validate_row(self, row: dict[str, str]) -> None:
        """Validate required fields in CSV row."""
        required = ["ident", "name", "latitude_deg", "longitude_deg", "iso_country"]
        for field in required:
            if not row.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Validate coordinate ranges
        try:
            lat = float(row["latitude_deg"])
            lon = float(row["longitude_deg"])
            if not (-90 <= lat <= 90):
                raise ValueError(f"Invalid latitude: {lat}")
            if not (-180 <= lon <= 180):
                raise ValueError(f"Invalid longitude: {lon}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid coordinates: {e}") from e

    def _upsert_airport(self, row: dict[str, str]) -> bool:
        """
        Upsert airport from CSV row.

        Returns True if created, False if updated.
        """
        ident = row["ident"]

        # Parse optional fields
        elevation = None
        if row.get("elevation_ft"):
            try:
                elevation = int(float(row["elevation_ft"]))
            except (ValueError, TypeError):
                pass

        # Prepare data
        data = {
            "name": row["name"],
            "airport_type": row.get("type", ""),
            "latitude_deg": float(row["latitude_deg"]),
            "longitude_deg": float(row["longitude_deg"]),
            "elevation_ft": elevation,
            "iata_code": row.get("iata_code", ""),
            "iso_country": row["iso_country"],
            "iso_region": row.get("iso_region", ""),
            "municipality": row.get("municipality", ""),
        }

        # Upsert
        airport, created = Airport.objects.update_or_create(
            ident=ident,
            defaults=data,
        )

        return created
