"""Tests for validate_airports management command."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.airports.models import Airport


class ValidateAirportsCommandTests(TestCase):
    """Test the validate_airports management command."""

    def test_validation_with_no_airports(self):
        """Test validation command with empty database."""
        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("Total airports in database: 0", output)
        self.assertIn("All validation checks passed!", output)

    def test_validation_with_valid_airports(self):
        """Test validation command with valid airport data."""
        # Create valid airports
        Airport.objects.create(
            ident="KDEN",
            iata_code="DEN",
            name="Denver International Airport",
            airport_type="large_airport",
            latitude_deg=39.8561,
            longitude_deg=-104.6737,
            iso_country="US",
            municipality="Denver",
        )
        Airport.objects.create(
            ident="KSFO",
            iata_code="SFO",
            name="San Francisco International Airport",
            airport_type="large_airport",
            latitude_deg=37.6213,
            longitude_deg=-122.3790,
            iso_country="US",
            municipality="San Francisco",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("Total airports in database: 2", output)
        self.assertIn("✓ All required fields present", output)
        self.assertIn("✓ All latitudes within valid range", output)
        self.assertIn("✓ All longitudes within valid range", output)
        self.assertIn("✓ All idents are unique", output)
        self.assertIn("✓ All IATA codes have valid format", output)
        self.assertIn("✓ All ISO country codes have valid format", output)
        self.assertIn("All validation checks passed!", output)

    def test_validation_with_invalid_latitude(self):
        """Test validation detects invalid latitude."""
        # Create airport with invalid latitude
        Airport.objects.create(
            ident="INVAL",
            name="Invalid Latitude Airport",
            airport_type="small_airport",
            latitude_deg=95.0,  # Invalid: > 90
            longitude_deg=-105.0,
            iso_country="US",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("⚠ 1 records with latitude out of range", output)
        self.assertIn("Found 1 types of anomalies", output)

    def test_validation_with_invalid_longitude(self):
        """Test validation detects invalid longitude."""
        # Create airport with invalid longitude
        Airport.objects.create(
            ident="INVAL",
            name="Invalid Longitude Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=185.0,  # Invalid: > 180
            iso_country="US",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("⚠ 1 records with longitude out of range", output)
        self.assertIn("Found 1 types of anomalies", output)

    def test_validation_with_invalid_iata_code(self):
        """Test validation detects invalid IATA code format."""
        # Create airport with invalid IATA code
        Airport.objects.create(
            ident="TEST1",
            iata_code="D1",  # Invalid: not 3 letters
            name="Test Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("⚠ 1 records with invalid IATA code format", output)
        self.assertIn("Found 1 types of anomalies", output)

    def test_validation_verbose_mode(self):
        """Test validation command with verbose flag shows details."""
        # Create multiple airports with issues
        for i in range(3):
            Airport.objects.create(
                ident=f"INV{i}",
                name=f"Invalid Airport {i}",
                airport_type="small_airport",
                latitude_deg=95.0,  # Invalid
                longitude_deg=-105.0,
                iso_country="US",
            )

        out = StringIO()
        call_command("validate_airports", "--verbose", stdout=out)
        output = out.getvalue()

        # Should show detailed records in verbose mode
        self.assertIn("INV0", output)
        self.assertIn("INV1", output)
        self.assertIn("INV2", output)

    def test_validation_iata_coverage_reporting(self):
        """Test validation reports IATA code coverage."""
        # Create airports with and without IATA codes
        Airport.objects.create(
            ident="KDEN",
            iata_code="DEN",
            name="Denver Airport",
            airport_type="large_airport",
            latitude_deg=39.8561,
            longitude_deg=-104.6737,
            iso_country="US",
        )
        Airport.objects.create(
            ident="00AA",
            iata_code="",
            name="Small Local Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("1 of 2 airports have IATA codes (50.0%)", output)

    def test_validation_multiple_anomalies(self):
        """Test validation detects multiple types of anomalies."""
        # Create airports with various issues
        Airport.objects.create(
            ident="INV1",
            iata_code="XX",  # Invalid IATA
            name="Invalid Airport 1",
            airport_type="small_airport",
            latitude_deg=95.0,  # Invalid latitude
            longitude_deg=-105.0,
            iso_country="US",
        )
        Airport.objects.create(
            ident="INV2",
            iata_code="YYY",
            name="Invalid Airport 2",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=190.0,  # Invalid longitude
            iso_country="X",  # Invalid country code
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("Found", output)
        self.assertIn("types of anomalies", output)
        # Should detect: invalid latitude, longitude, IATA, and country code
        self.assertIn("Invalid latitude", output)
        self.assertIn("Invalid longitude", output)
        self.assertIn("Invalid IATA codes", output)
        self.assertIn("Invalid country codes", output)

    def test_validation_edge_case_coordinates(self):
        """Test validation accepts valid edge case coordinates."""
        # Create airports at edge cases
        Airport.objects.create(
            ident="NORTH",
            name="North Pole Airport",
            airport_type="small_airport",
            latitude_deg=90.0,  # Valid edge
            longitude_deg=0.0,
            iso_country="GL",
        )
        Airport.objects.create(
            ident="SOUTH",
            name="South Pole Airport",
            airport_type="small_airport",
            latitude_deg=-90.0,  # Valid edge
            longitude_deg=180.0,  # Valid edge
            iso_country="AQ",
        )

        out = StringIO()
        call_command("validate_airports", stdout=out)
        output = out.getvalue()

        self.assertIn("✓ All latitudes within valid range", output)
        self.assertIn("✓ All longitudes within valid range", output)
        self.assertIn("All validation checks passed!", output)
