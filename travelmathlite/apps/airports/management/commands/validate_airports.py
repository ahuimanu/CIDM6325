"""Management command to validate airport data and report anomalies."""

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.airports.models import Airport


class Command(BaseCommand):
    """Validate airport data and report anomalies."""

    help = "Validate airport data quality and report anomalies"

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed anomaly information",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the validation command."""
        verbose = options.get("verbose", False)
        anomalies: list[str] = []

        self.stdout.write("=" * 60)
        self.stdout.write("Airport Data Validation Report")
        self.stdout.write("=" * 60)
        self.stdout.write("")

        # Check total record count
        total_count = Airport.objects.count()
        self.stdout.write(f"Total airports in database: {total_count}")
        self.stdout.write("")

        # Validate required fields
        self.stdout.write("1. Checking required fields...")
        missing_fields = Airport.objects.filter(
            Q(ident="") | Q(name="") | Q(airport_type="") | Q(latitude_deg__isnull=True) | Q(longitude_deg__isnull=True) | Q(iso_country="")
        )
        if missing_fields.exists():
            count = missing_fields.count()
            anomalies.append(f"Missing required fields: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records missing required fields"))
            if verbose:
                for airport in missing_fields[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name}")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All required fields present"))

        # Validate latitude range (-90 to 90)
        self.stdout.write("")
        self.stdout.write("2. Checking latitude coordinate range...")
        invalid_lat = Airport.objects.filter(Q(latitude_deg__lt=-90) | Q(latitude_deg__gt=90))
        if invalid_lat.exists():
            count = invalid_lat.count()
            anomalies.append(f"Invalid latitude: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records with latitude out of range (-90 to 90)"))
            if verbose:
                for airport in invalid_lat[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name} (lat={airport.latitude_deg})")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All latitudes within valid range"))

        # Validate longitude range (-180 to 180)
        self.stdout.write("")
        self.stdout.write("3. Checking longitude coordinate range...")
        invalid_lon = Airport.objects.filter(Q(longitude_deg__lt=-180) | Q(longitude_deg__gt=180))
        if invalid_lon.exists():
            count = invalid_lon.count()
            anomalies.append(f"Invalid longitude: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records with longitude out of range (-180 to 180)"))
            if verbose:
                for airport in invalid_lon[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name} (lon={airport.longitude_deg})")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All longitudes within valid range"))

        # Check for null coordinates (should not happen if required fields check passes)
        self.stdout.write("")
        self.stdout.write("4. Checking for null coordinates...")
        null_coords = Airport.objects.filter(Q(latitude_deg__isnull=True) | Q(longitude_deg__isnull=True))
        if null_coords.exists():
            count = null_coords.count()
            anomalies.append(f"Null coordinates: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records with null coordinates"))
            if verbose:
                for airport in null_coords[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name}")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ No null coordinates found"))

        # Check uniqueness of ident (should be enforced by DB, but verify)
        self.stdout.write("")
        self.stdout.write("5. Checking ident uniqueness...")
        from django.db.models import Count

        duplicate_idents = Airport.objects.values("ident").annotate(count=Count("ident")).filter(count__gt=1)
        if duplicate_idents.exists():
            count = duplicate_idents.count()
            anomalies.append(f"Duplicate idents: {count} values")
            self.stdout.write(self.style.ERROR(f"   ✗ {count} duplicate ident values found!"))
            if verbose:
                for dup in duplicate_idents[:10]:
                    self.stdout.write(f"      - {dup['ident']}: {dup['count']} occurrences")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All idents are unique"))

        # Check IATA code format (3 letters when present)
        self.stdout.write("")
        self.stdout.write("6. Checking IATA code format...")
        invalid_iata = Airport.objects.exclude(iata_code="").exclude(iata_code__regex=r"^[A-Z]{3}$")
        if invalid_iata.exists():
            count = invalid_iata.count()
            anomalies.append(f"Invalid IATA codes: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records with invalid IATA code format"))
            if verbose:
                for airport in invalid_iata[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name} (IATA={airport.iata_code})")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All IATA codes have valid format"))

        # Check for missing IATA codes (informational, not an error)
        self.stdout.write("")
        self.stdout.write("7. Checking IATA code coverage...")
        missing_iata = Airport.objects.filter(iata_code="")
        missing_count = missing_iata.count()
        has_iata = total_count - missing_count
        if total_count > 0:
            coverage = (has_iata / total_count) * 100
            self.stdout.write(f"   ℹ {has_iata} of {total_count} airports have IATA codes ({coverage:.1f}%)")
        else:
            self.stdout.write("   ℹ No airports in database")

        # Check ISO country code format (2 letters)
        self.stdout.write("")
        self.stdout.write("8. Checking ISO country code format...")
        invalid_country = Airport.objects.exclude(iso_country__regex=r"^[A-Z]{2}$")
        if invalid_country.exists():
            count = invalid_country.count()
            anomalies.append(f"Invalid country codes: {count} records")
            self.stdout.write(self.style.WARNING(f"   ⚠ {count} records with invalid ISO country code format"))
            if verbose:
                for airport in invalid_country[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name} (country={airport.iso_country})")
                if count > 10:
                    self.stdout.write(f"      ... and {count - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All ISO country codes have valid format"))

        # Normalized country links
        self.stdout.write("")
        self.stdout.write("9. Checking normalized Country links...")
        linked_countries = Airport.objects.filter(country__isnull=False).count()
        missing_country_links = total_count - linked_countries
        if missing_country_links:
            pct = (linked_countries / total_count) * 100 if total_count else 0
            self.stdout.write(self.style.WARNING(f"   ⚠ {linked_countries} linked / {total_count} total ({pct:.1f}% linkage)"))
            if verbose:
                for airport in Airport.objects.filter(country__isnull=True)[:10]:
                    self.stdout.write(f"      - {airport.ident}: {airport.name} missing Country link (iso_country={airport.iso_country})")
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All airports linked to normalized Country records"))

        # Normalized city links
        self.stdout.write("")
        self.stdout.write("10. Checking normalized City links...")
        airports_with_municipality = Airport.objects.exclude(municipality="")
        total_with_municipality = airports_with_municipality.count()
        linked_cities = airports_with_municipality.filter(city__isnull=False).count()
        missing_city_links = total_with_municipality - linked_cities
        if missing_city_links:
            pct = (linked_cities / total_with_municipality) * 100 if total_with_municipality else 0
            self.stdout.write(
                self.style.WARNING(f"   ⚠ {linked_cities} linked / {total_with_municipality} with municipality ({pct:.1f}% linkage)")
            )
            if verbose:
                for airport in airports_with_municipality.filter(city__isnull=True)[:10]:
                    self.stdout.write(
                        f"      - {airport.ident}: {airport.name} missing City link (municipality={airport.municipality or 'N/A'})"
                    )
        else:
            self.stdout.write(self.style.SUCCESS("   ✓ All airports with municipality values linked to normalized City records"))

        # Summary
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("Validation Summary")
        self.stdout.write("=" * 60)

        if anomalies:
            self.stdout.write(self.style.WARNING(f"Found {len(anomalies)} types of anomalies:"))
            for anomaly in anomalies:
                self.stdout.write(f"  - {anomaly}")
            self.stdout.write("")
            self.stdout.write("Run with --verbose to see detailed records.")
        else:
            self.stdout.write(self.style.SUCCESS("✓ All validation checks passed!"))

        self.stdout.write("")
