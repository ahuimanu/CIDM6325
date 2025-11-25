"""Django management command to import airports from OurAirports CSV."""

import csv
import logging
import ssl
from typing import Any
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandParser

from apps.airports.models import Airport
from apps.airports.services import AirportLocationIntegrator, LocationLink
from apps.base.models import City, Country

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
        parser.add_argument(
            "--skip-country-link",
            action="store_true",
            help="Skip creating/linking normalized Country rows",
        )
        parser.add_argument(
            "--skip-city-link",
            action="store_true",
            help="Skip creating/linking normalized City rows",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the import command."""
        dry_run = options["dry_run"]
        filter_iata = options["filter_iata"]
        limit = options.get("limit")
        local_file = options.get("file")
        url = options["url"]
        skip_country_link = options.get("skip_country_link", False)
        skip_city_link = options.get("skip_city_link", False)

        integrator: AirportLocationIntegrator | None = None
        if not dry_run and not (skip_country_link and skip_city_link):
            integrator = AirportLocationIntegrator()

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
            "country_links": 0,
            "countries_created": 0,
            "city_links": 0,
            "cities_created": 0,
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
                        self.stdout.write(f"[DRY RUN] Would process: {row.get('name')} ({row.get('iata_code') or row.get('ident')})")
                    else:
                        country = None
                        city = None
                        location_link: LocationLink | None = None
                        if integrator:
                            location_link = integrator.link_location(
                                iso_country=row.get("iso_country"),
                                municipality=row.get("municipality"),
                                latitude=self._safe_float(row.get("latitude_deg")),
                                longitude=self._safe_float(row.get("longitude_deg")),
                                link_country=not skip_country_link,
                                link_city=not skip_city_link,
                            )
                            country, city = location_link.country, location_link.city
                            self._update_integration_stats(stats, location_link)

                        created = self._upsert_airport(
                            row,
                            country=country,
                            city=city,
                            active=self._is_active(row),
                        )
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

        processed_rows = max(stats["total"] - stats["skipped"] - stats["errors"], 0)
        if processed_rows and not dry_run:
            country_pct = (stats["country_links"] / processed_rows) * 100 if processed_rows else 0
            city_pct = (stats["city_links"] / processed_rows) * 100 if processed_rows else 0
            self.stdout.write(
                f"Country links: {stats['country_links']}/{processed_rows} ({country_pct:.1f}%) (created {stats['countries_created']})"
            )
            self.stdout.write(f"City links: {stats['city_links']}/{processed_rows} ({city_pct:.1f}%) (created {stats['cities_created']})")
        elif dry_run:
            self.stdout.write(self.style.WARNING("Location linking skipped during dry-run"))

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

    def _unsafe_float(self, value: str | None) -> float | None:
        """Convert value to float if possible."""
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _safe_float(self, value: str | None) -> float | None:
        """Wrapper for compatibility (public helper)."""
        return self._unsafe_float(value)

    def _is_active(self, row: dict[str, str]) -> bool:
        """Determine whether the airport should be marked active."""
        return row.get("type", "").lower() != "closed"

    def _update_integration_stats(self, stats: dict[str, int], link: LocationLink | None) -> None:
        """Update counters for normalized Country/City linkage."""
        if not link:
            return
        if link.country:
            stats["country_links"] += 1
        if link.city:
            stats["city_links"] += 1
        if link.created_country:
            stats["countries_created"] += 1
        if link.created_city:
            stats["cities_created"] += 1

    def _upsert_airport(
        self,
        row: dict[str, str],
        *,
        country: Country | None = None,
        city: City | None = None,
        active: bool = True,
    ) -> bool:
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
            "country": country,
            "city": city,
            "active": active,
        }

        # Upsert
        airport, created = Airport.objects.update_or_create(
            ident=ident,
            defaults=data,
        )

        return created
