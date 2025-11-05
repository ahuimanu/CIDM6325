"""Data validation tests for Airport model."""

from django.db import IntegrityError
from django.test import TestCase

from apps.airports.models import Airport


class AirportValidationTests(TestCase):
    """Test data validation rules for airports."""

    def test_required_fields_present(self):
        """Test that required fields are enforced."""
        airport = Airport(
            ident="TEST",
            name="Test Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )
        # Should not raise
        airport.full_clean()
        airport.save()
        self.assertEqual(Airport.objects.count(), 1)

    def test_latitude_within_range(self):
        """Test that latitude is within valid range."""
        # Valid latitude
        airport = Airport.objects.create(
            ident="TEST1",
            name="Test Airport 1",
            airport_type="small_airport",
            latitude_deg=45.5,
            longitude_deg=-105.0,
            iso_country="US",
        )
        self.assertEqual(airport.latitude_deg, 45.5)

        # Edge cases
        airport_north = Airport.objects.create(
            ident="NORTH",
            name="North Pole Airport",
            airport_type="small_airport",
            latitude_deg=90.0,
            longitude_deg=0.0,
            iso_country="GL",
        )
        self.assertEqual(airport_north.latitude_deg, 90.0)

        airport_south = Airport.objects.create(
            ident="SOUTH",
            name="South Pole Airport",
            airport_type="small_airport",
            latitude_deg=-90.0,
            longitude_deg=0.0,
            iso_country="AQ",
        )
        self.assertEqual(airport_south.latitude_deg, -90.0)

    def test_longitude_within_range(self):
        """Test that longitude is within valid range."""
        # Valid longitude
        airport = Airport.objects.create(
            ident="TEST2",
            name="Test Airport 2",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-122.5,
            iso_country="US",
        )
        self.assertEqual(airport.longitude_deg, -122.5)

        # Edge cases
        airport_east = Airport.objects.create(
            ident="EAST",
            name="East Edge Airport",
            airport_type="small_airport",
            latitude_deg=0.0,
            longitude_deg=180.0,
            iso_country="FJ",
        )
        self.assertEqual(airport_east.longitude_deg, 180.0)

        airport_west = Airport.objects.create(
            ident="WEST",
            name="West Edge Airport",
            airport_type="small_airport",
            latitude_deg=0.0,
            longitude_deg=-180.0,
            iso_country="FJ",
        )
        self.assertEqual(airport_west.longitude_deg, -180.0)

    def test_ident_uniqueness(self):
        """Test that ident is unique."""
        Airport.objects.create(
            ident="UNIQUE",
            name="First Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )

        # Duplicate ident should fail
        with self.assertRaises(IntegrityError):
            Airport.objects.create(
                ident="UNIQUE",
                name="Second Airport",
                airport_type="small_airport",
                latitude_deg=41.0,
                longitude_deg=-106.0,
                iso_country="US",
            )

    def test_iata_code_optional(self):
        """Test that IATA code is optional."""
        airport = Airport.objects.create(
            ident="NOCODE",
            name="No IATA Code Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
            iata_code="",
        )
        self.assertEqual(airport.iata_code, "")

    def test_string_representation_with_iata(self):
        """Test string representation with IATA code."""
        airport = Airport.objects.create(
            ident="KDEN",
            iata_code="DEN",
            name="Denver International Airport",
            airport_type="large_airport",
            latitude_deg=39.8561,
            longitude_deg=-104.6737,
            iso_country="US",
        )
        self.assertEqual(str(airport), "Denver International Airport (DEN)")

    def test_string_representation_without_iata(self):
        """Test string representation without IATA code."""
        airport = Airport.objects.create(
            ident="00AA",
            iata_code="",
            name="Small Local Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )
        self.assertEqual(str(airport), "Small Local Airport (00AA)")

    def test_elevation_optional(self):
        """Test that elevation is optional."""
        airport = Airport.objects.create(
            ident="NOEL",
            name="No Elevation Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )
        self.assertIsNone(airport.elevation_ft)

    def test_municipality_optional(self):
        """Test that municipality is optional."""
        airport = Airport.objects.create(
            ident="NOMUN",
            name="No Municipality Airport",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )
        self.assertEqual(airport.municipality, "")
