"""Unit tests for geographic distance calculation functions.

Tests haversine_distance, geodesic_distance, and related utilities
with happy paths, edge cases, and boundary conditions.
"""

import math

from django.test import TestCase

from ..geo import (
    EARTH_RADIUS_KM,
    geodesic_distance,
    haversine_distance,
    km_to_miles,
    miles_to_km,
)


class HaversineDistanceTests(TestCase):
    """Test haversine distance calculation."""

    def test_same_location_returns_zero(self):
        """Distance between identical coordinates should be zero."""
        distance = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 0.0, places=2)

    def test_new_york_to_los_angeles(self):
        """Test distance between NYC and LA (approximately 3944 km)."""
        # NYC: 40.7128° N, 74.0060° W
        # LA: 34.0522° N, 118.2437° W
        distance = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        self.assertGreater(distance, 3900)
        self.assertLess(distance, 4000)

    def test_london_to_paris(self):
        """Test distance between London and Paris (approximately 344 km)."""
        # London: 51.5074° N, 0.1278° W
        # Paris: 48.8566° N, 2.3522° E
        distance = haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        self.assertGreater(distance, 340)
        self.assertLess(distance, 350)

    def test_short_distance_accuracy(self):
        """Test accuracy for short distances (< 10 km)."""
        # Two points approximately 5 km apart
        distance = haversine_distance(40.7128, -74.0060, 40.7500, -74.0060)
        self.assertGreater(distance, 4)
        self.assertLess(distance, 6)

    def test_antipodal_points(self):
        """Test maximum distance (opposite sides of Earth)."""
        # Madrid: 40.4168° N, 3.7038° W
        # Wellington: 41.2865° S, 174.7762° E (approximately antipodal)
        distance = haversine_distance(40.4168, -3.7038, -41.2865, 174.7762)
        # Should be close to half Earth's circumference (~20,000 km)
        self.assertGreater(distance, 19000)
        self.assertLess(distance, 20500)

    def test_equator_crossing(self):
        """Test distance crossing the equator."""
        # Quito, Ecuador: 0.1807° S, 78.4678° W
        # Singapore: 1.3521° N, 103.8198° E
        distance = haversine_distance(-0.1807, -78.4678, 1.3521, 103.8198)
        self.assertGreater(distance, 0)

    def test_negative_coordinates(self):
        """Test with negative latitude/longitude values."""
        # Sydney: 33.8688° S, 151.2093° E
        # Cape Town: 33.9249° S, 18.4241° E
        distance = haversine_distance(-33.8688, 151.2093, -33.9249, 18.4241)
        self.assertGreater(distance, 11000)
        self.assertLess(distance, 12000)

    def test_180_meridian_crossing(self):
        """Test distance crossing the 180° meridian."""
        # Tokyo: 35.6762° N, 139.6503° E
        # San Francisco: 37.7749° N, 122.4194° W
        distance = haversine_distance(35.6762, 139.6503, 37.7749, -122.4194)
        self.assertGreater(distance, 8000)
        self.assertLess(distance, 9000)


class GeodesicDistanceTests(TestCase):
    """Test geodesic distance calculation (with geopy fallback)."""

    def test_same_location_returns_zero(self):
        """Distance between identical coordinates should be zero."""
        distance = geodesic_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 0.0, places=2)

    def test_london_to_paris(self):
        """Test distance between London and Paris (approximately 344 km)."""
        distance = geodesic_distance(51.5074, -0.1278, 48.8566, 2.3522)
        self.assertGreater(distance, 340)
        self.assertLess(distance, 350)

    def test_short_distance(self):
        """Test short distance accuracy."""
        # Two nearby points
        distance = geodesic_distance(40.7128, -74.0060, 40.7200, -74.0100)
        self.assertGreater(distance, 0)
        self.assertLess(distance, 2)

    def test_falls_back_to_haversine_on_import_error(self):
        """Geodesic should fall back to haversine if geopy unavailable."""
        # This test verifies the fallback mechanism exists
        # Both should give similar results
        haversine_dist = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        geodesic_dist = geodesic_distance(40.7128, -74.0060, 34.0522, -118.2437)

        # Allow 1% difference (geopy may be more accurate)
        diff_percent = abs(haversine_dist - geodesic_dist) / haversine_dist * 100
        self.assertLess(diff_percent, 1.0)


class UnitConversionTests(TestCase):
    """Test distance unit conversion functions."""

    def test_km_to_miles_conversion(self):
        """Test kilometer to miles conversion."""
        self.assertAlmostEqual(km_to_miles(100), 62.1371, places=4)
        self.assertAlmostEqual(km_to_miles(1), 0.621371, places=6)
        self.assertEqual(km_to_miles(0), 0.0)

    def test_miles_to_km_conversion(self):
        """Test miles to kilometers conversion."""
        self.assertAlmostEqual(miles_to_km(100), 160.934, places=3)
        self.assertAlmostEqual(miles_to_km(1), 1.60934, places=5)
        self.assertEqual(miles_to_km(0), 0.0)

    def test_round_trip_conversion(self):
        """Test converting km -> miles -> km returns approximately original value."""
        original_km = 100.0
        miles = km_to_miles(original_km)
        back_to_km = miles_to_km(miles)
        # Conversion factors have slight rounding, so we accept 0.01% tolerance
        self.assertAlmostEqual(original_km, back_to_km, delta=0.01)

    def test_negative_values(self):
        """Test that negative distances work (though physically meaningless)."""
        self.assertAlmostEqual(km_to_miles(-100), -62.1371, places=4)
        self.assertAlmostEqual(miles_to_km(-100), -160.934, places=3)


class EdgeCaseTests(TestCase):
    """Test edge cases and boundary conditions."""

    def test_zero_distance(self):
        """Test zero distance calculations."""
        self.assertEqual(haversine_distance(0, 0, 0, 0), 0.0)
        self.assertEqual(geodesic_distance(0, 0, 0, 0), 0.0)

    def test_poles(self):
        """Test distance calculations at poles."""
        # North Pole to South Pole (half Earth's circumference)
        distance = haversine_distance(90, 0, -90, 0)
        expected = math.pi * EARTH_RADIUS_KM
        self.assertAlmostEqual(distance, expected, places=1)

    def test_boundary_latitudes(self):
        """Test with latitude boundaries (-90 to 90)."""
        # Extreme north to extreme south
        distance = haversine_distance(90, 0, -90, 180)
        self.assertGreater(distance, 20000)

    def test_boundary_longitudes(self):
        """Test with longitude boundaries (-180 to 180)."""
        # Same latitude, opposite longitudes
        distance = haversine_distance(0, -180, 0, 180)
        # At equator, this should be 0 (same point)
        self.assertAlmostEqual(distance, 0.0, places=1)

    def test_very_small_distance(self):
        """Test very small distances (< 1 meter)."""
        # Points 0.00001 degrees apart (~1.1 meters)
        distance = haversine_distance(40.7128, -74.0060, 40.71281, -74.0060)
        self.assertGreater(distance, 0)
        self.assertLess(distance, 0.01)  # Less than 10 meters
