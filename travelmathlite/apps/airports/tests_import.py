"""Tests for import_airports management command."""

import csv
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from apps.airports.models import Airport


class ImportAirportsCommandTests(TestCase):
    """Test the import_airports management command."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_csv_data = [
            {
                "id": "1",
                "ident": "TEST1",
                "type": "small_airport",
                "name": "Test Airport One",
                "latitude_deg": "40.0",
                "longitude_deg": "-105.0",
                "elevation_ft": "5000",
                "iso_country": "US",
                "iso_region": "US-CO",
                "municipality": "TestCity",
                "iata_code": "TS1",
            },
            {
                "id": "2",
                "ident": "TEST2",
                "type": "medium_airport",
                "name": "Test Airport Two",
                "latitude_deg": "41.0",
                "longitude_deg": "-106.0",
                "elevation_ft": "",
                "iso_country": "US",
                "iso_region": "US-WY",
                "municipality": "",
                "iata_code": "",
            },
        ]

    def _create_test_csv(self) -> Path:
        """Create a temporary CSV file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="")
        writer = csv.DictWriter(temp_file, fieldnames=self.test_csv_data[0].keys())
        writer.writeheader()
        writer.writerows(self.test_csv_data)
        temp_file.close()
        return Path(temp_file.name)

    def test_import_dry_run(self):
        """Test dry-run mode doesn't save to database."""
        csv_file = self._create_test_csv()

        try:
            out = StringIO()
            call_command(
                "import_airports",
                file=str(csv_file),
                dry_run=True,
                stdout=out,
            )

            output = out.getvalue()
            self.assertIn("[DRY RUN]", output)
            self.assertIn("Test Airport One", output)
            self.assertEqual(Airport.objects.count(), 0)
        finally:
            csv_file.unlink()

    def test_import_creates_airports(self):
        """Test that import creates airport records."""
        csv_file = self._create_test_csv()

        try:
            out = StringIO()
            call_command(
                "import_airports",
                file=str(csv_file),
                stdout=out,
            )

            output = out.getvalue()
            self.assertIn("Created: 2", output)
            self.assertEqual(Airport.objects.count(), 2)

            airport1 = Airport.objects.get(ident="TEST1")
            self.assertEqual(airport1.name, "Test Airport One")
            self.assertEqual(airport1.iata_code, "TS1")
            self.assertEqual(airport1.latitude_deg, 40.0)
        finally:
            csv_file.unlink()

    def test_import_idempotent(self):
        """Test that running import twice is idempotent."""
        csv_file = self._create_test_csv()

        try:
            # First import
            call_command("import_airports", file=str(csv_file), stdout=StringIO())
            self.assertEqual(Airport.objects.count(), 2)

            # Second import (should update, not duplicate)
            out = StringIO()
            call_command("import_airports", file=str(csv_file), stdout=out)

            output = out.getvalue()
            self.assertIn("Updated: 2", output)
            self.assertEqual(Airport.objects.count(), 2)
        finally:
            csv_file.unlink()

    def test_import_with_limit(self):
        """Test that limit parameter works."""
        csv_file = self._create_test_csv()

        try:
            out = StringIO()
            call_command(
                "import_airports",
                file=str(csv_file),
                limit=1,
                stdout=out,
            )

            output = out.getvalue()
            self.assertIn("Total rows: 2", output)  # Read 2, limited to 1
            self.assertEqual(Airport.objects.count(), 1)
        finally:
            csv_file.unlink()

    def test_import_filter_iata(self):
        """Test filtering by IATA code."""
        csv_file = self._create_test_csv()

        try:
            out = StringIO()
            call_command(
                "import_airports",
                file=str(csv_file),
                filter_iata=True,
                stdout=out,
            )

            output = out.getvalue()
            self.assertIn("Skipped: 1", output)
            self.assertEqual(Airport.objects.count(), 1)

            # Only TEST1 should be imported (has IATA code)
            self.assertTrue(Airport.objects.filter(ident="TEST1").exists())
            self.assertFalse(Airport.objects.filter(ident="TEST2").exists())
        finally:
            csv_file.unlink()

    def test_import_skips_invalid_coordinates(self):
        """Test that rows with invalid coordinates are skipped."""
        invalid_data = [
            {
                "id": "3",
                "ident": "INVALID",
                "type": "small_airport",
                "name": "Invalid Airport",
                "latitude_deg": "999.0",  # Invalid
                "longitude_deg": "-105.0",
                "elevation_ft": "",
                "iso_country": "US",
                "iso_region": "",
                "municipality": "",
                "iata_code": "",
            }
        ]

        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="")
        writer = csv.DictWriter(temp_file, fieldnames=invalid_data[0].keys())
        writer.writeheader()
        writer.writerows(invalid_data)
        temp_file.close()
        csv_file = Path(temp_file.name)

        try:
            out = StringIO()
            call_command("import_airports", file=str(csv_file), stdout=out)

            output = out.getvalue()
            self.assertIn("Errors: 1", output)
            self.assertEqual(Airport.objects.count(), 0)
        finally:
            csv_file.unlink()

    def test_import_handles_missing_required_fields(self):
        """Test that rows with missing required fields are skipped."""
        incomplete_data = [
            {
                "id": "4",
                "ident": "",  # Missing required field
                "type": "small_airport",
                "name": "Incomplete Airport",
                "latitude_deg": "40.0",
                "longitude_deg": "-105.0",
                "elevation_ft": "",
                "iso_country": "US",
                "iso_region": "",
                "municipality": "",
                "iata_code": "",
            }
        ]

        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="")
        writer = csv.DictWriter(temp_file, fieldnames=incomplete_data[0].keys())
        writer.writeheader()
        writer.writerows(incomplete_data)
        temp_file.close()
        csv_file = Path(temp_file.name)

        try:
            out = StringIO()
            call_command("import_airports", file=str(csv_file), stdout=out)

            output = out.getvalue()
            self.assertIn("Errors: 1", output)
            self.assertEqual(Airport.objects.count(), 0)
        finally:
            csv_file.unlink()
