"""Tests for schema mapping and normalization."""

from typing import Any, cast

from django.test import TestCase

from apps.airports.schema_mapping import (
    FIELD_MAPPING,
    MAPPING_EXAMPLE,
    UNMAPPED_FIELDS,
    normalize_csv_row,
)


class SchemaMapingDocumentationTests(TestCase):
    """Test schema mapping documentation and constants."""

    def test_field_mapping_structure(self):
        """Test that FIELD_MAPPING has all expected model fields."""
        expected_fields = [
            "ident",
            "iata_code",
            "name",
            "airport_type",
            "latitude_deg",
            "longitude_deg",
            "elevation_ft",
            "iso_country",
            "iso_region",
            "municipality",
        ]

        for field in expected_fields:
            self.assertIn(field, FIELD_MAPPING)
            self.assertIn("csv_field", FIELD_MAPPING[field])
            self.assertIn("description", FIELD_MAPPING[field])

    def test_required_fields_documented(self):
        """Test that required fields are properly marked."""
        required_fields = ["ident", "name", "latitude_deg", "longitude_deg", "iso_country"]

        for field in required_fields:
            self.assertTrue(FIELD_MAPPING[field]["required"])

    def test_unmapped_fields_list(self):
        """Test that unmapped fields are documented."""
        expected_unmapped = [
            "id",
            "continent",
            "scheduled_service",
            "gps_code",
            "local_code",
            "home_link",
            "wikipedia_link",
            "keywords",
        ]

        for field in expected_unmapped:
            self.assertIn(field, UNMAPPED_FIELDS)

    def test_mapping_example_structure(self):
        """Test that MAPPING_EXAMPLE has proper structure."""
        self.assertIn("csv_input", MAPPING_EXAMPLE)
        self.assertIn("model_output", MAPPING_EXAMPLE)

        # Check CSV input has OurAirports fields
        csv_input = MAPPING_EXAMPLE["csv_input"]
        self.assertIn("ident", csv_input)
        self.assertIn("iata_code", csv_input)
        self.assertIn("latitude_deg", csv_input)

        # Check model output has our model fields
        model_output = MAPPING_EXAMPLE["model_output"]
        self.assertIn("ident", model_output)
        self.assertIn("airport_type", model_output)
        self.assertEqual(model_output["ident"], "KDEN")


class NormalizeCsvRowTests(TestCase):
    """Test the normalize_csv_row function."""

    def test_normalize_complete_row(self):
        """Test normalizing a complete CSV row."""
        csv_row = {
            "ident": "KDEN",
            "type": "large_airport",
            "name": "Denver International Airport",
            "latitude_deg": "39.8561",
            "longitude_deg": "-104.6737",
            "elevation_ft": "5434",
            "iso_country": "US",
            "iso_region": "US-CO",
            "municipality": "Denver",
            "iata_code": "DEN",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertEqual(result["ident"], "KDEN")
        self.assertEqual(result["iata_code"], "DEN")
        self.assertEqual(result["name"], "Denver International Airport")
        self.assertEqual(result["airport_type"], "large_airport")
        self.assertAlmostEqual(result["latitude_deg"], 39.8561)
        self.assertAlmostEqual(result["longitude_deg"], -104.6737)
        self.assertEqual(result["elevation_ft"], 5434)
        self.assertEqual(result["iso_country"], "US")
        self.assertEqual(result["iso_region"], "US-CO")
        self.assertEqual(result["municipality"], "Denver")

    def test_normalize_minimal_row(self):
        """Test normalizing a row with only required fields."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertEqual(result["ident"], "TEST")
        self.assertEqual(result["name"], "Test Airport")
        self.assertEqual(result["latitude_deg"], 40.0)
        self.assertEqual(result["longitude_deg"], -105.0)
        self.assertEqual(result["iso_country"], "US")
        self.assertEqual(result["iata_code"], "")
        self.assertEqual(result["airport_type"], "")
        self.assertIsNone(result["elevation_ft"])

    def test_normalize_with_empty_optional_fields(self):
        """Test normalization handles empty optional fields."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
            "iata_code": "",
            "type": "",
            "elevation_ft": "",
            "iso_region": "",
            "municipality": "",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertEqual(result["iata_code"], "")
        self.assertEqual(result["airport_type"], "")
        self.assertIsNone(result["elevation_ft"])
        self.assertEqual(result["iso_region"], "")
        self.assertEqual(result["municipality"], "")

    def test_normalize_coordinate_conversion(self):
        """Test that string coordinates are converted to float."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "45.5",
            "longitude_deg": "-122.5",
            "iso_country": "US",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertIsInstance(result["latitude_deg"], float)
        self.assertIsInstance(result["longitude_deg"], float)
        self.assertEqual(result["latitude_deg"], 45.5)
        self.assertEqual(result["longitude_deg"], -122.5)

    def test_normalize_elevation_conversion(self):
        """Test elevation string to int conversion."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
            "elevation_ft": "5280.5",  # Float string
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertIsInstance(result["elevation_ft"], int)
        self.assertEqual(result["elevation_ft"], 5280)

    def test_normalize_invalid_elevation(self):
        """Test that invalid elevation becomes None."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
            "elevation_ft": "invalid",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertIsNone(result["elevation_ft"])

    def test_normalize_invalid_latitude(self):
        """Test that invalid latitude raises ValueError."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "95.0",  # Invalid: > 90
            "longitude_deg": "-105.0",
            "iso_country": "US",
        }

        with self.assertRaises(ValueError) as context:
            normalize_csv_row(csv_row)

        self.assertIn("Invalid latitude", str(context.exception))

    def test_normalize_invalid_longitude(self):
        """Test that invalid longitude raises ValueError."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "185.0",  # Invalid: > 180
            "iso_country": "US",
        }

        with self.assertRaises(ValueError) as context:
            normalize_csv_row(csv_row)

        self.assertIn("Invalid longitude", str(context.exception))

    def test_normalize_edge_case_coordinates(self):
        """Test normalization accepts valid edge case coordinates."""
        csv_row = {
            "ident": "NORTH",
            "name": "North Pole Airport",
            "latitude_deg": "90.0",  # Valid edge
            "longitude_deg": "180.0",  # Valid edge
            "iso_country": "GL",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertEqual(result["latitude_deg"], 90.0)
        self.assertEqual(result["longitude_deg"], 180.0)

    def test_normalize_field_name_mapping(self):
        """Test that CSV field 'type' maps to model field 'airport_type'."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "type": "small_airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        self.assertEqual(result["airport_type"], "small_airport")
        self.assertNotIn("type", result)

    def test_normalize_preserves_all_model_fields(self):
        """Test that all model fields are present in normalized output."""
        csv_row = {
            "ident": "TEST",
            "name": "Test Airport",
            "latitude_deg": "40.0",
            "longitude_deg": "-105.0",
            "iso_country": "US",
        }

        result = cast(dict[str, Any], normalize_csv_row(csv_row))

        expected_fields = [
            "ident",
            "iata_code",
            "name",
            "airport_type",
            "latitude_deg",
            "longitude_deg",
            "elevation_ft",
            "iso_country",
            "iso_region",
            "municipality",
        ]

        for field in expected_fields:
            self.assertIn(field, result)


class SchemaIntegrationTests(TestCase):
    """Test schema mapping integration with import command logic."""

    def test_mapping_matches_import_command(self):
        """Test that normalize_csv_row output matches import command expectations."""
        from apps.airports.models import Airport

        csv_row = {
            "ident": "KDEN",
            "type": "large_airport",
            "name": "Denver International Airport",
            "latitude_deg": "39.8561",
            "longitude_deg": "-104.6737",
            "elevation_ft": "5434",
            "iso_country": "US",
            "iso_region": "US-CO",
            "municipality": "Denver",
            "iata_code": "DEN",
        }

        normalized = cast(dict[str, Any], normalize_csv_row(csv_row))

        # Create airport using normalized data
        airport = Airport.objects.create(
            ident=normalized["ident"],
            **{k: v for k, v in normalized.items() if k != "ident"},
        )

        self.assertEqual(airport.ident, "KDEN")
        self.assertEqual(airport.iata_code, "DEN")
        self.assertEqual(airport.name, "Denver International Airport")
        self.assertEqual(airport.airport_type, "large_airport")
        self.assertAlmostEqual(airport.latitude_deg, 39.8561)
        self.assertAlmostEqual(airport.longitude_deg, -104.6737)
        self.assertEqual(airport.elevation_ft, 5434)
        self.assertEqual(airport.iso_country, "US")

    def test_all_field_mappings_documented(self):
        """Test that all Airport model fields are documented in FIELD_MAPPING."""
        from apps.airports.models import Airport

        # Get model fields (excluding auto fields)
        model_fields = {
            f.name for f in Airport._meta.get_fields() if not f.auto_created and f.name not in ["id", "created_at", "updated_at"]
        }

        # Get documented fields
        documented_fields = set(FIELD_MAPPING.keys())

        # Should match
        self.assertEqual(model_fields, documented_fields)
