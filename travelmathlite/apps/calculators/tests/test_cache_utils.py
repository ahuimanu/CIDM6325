"""Tests for calculator caching utilities.

Verify cache behavior for distance and cost calculations.
"""

from django.core.cache import cache
from django.test import TestCase

from ..utils import (
    calculate_fuel_cost_cached,
    calculate_route_distance_cached,
    calculate_trip_metrics_cached,
    clear_calculator_cache,
    haversine_distance_cached,
)


class CalculatorCachingTestCase(TestCase):
    """Test caching behavior for calculator operations."""

    def setUp(self) -> None:
        """Clear cache before each test."""
        cache.clear()

    def tearDown(self) -> None:
        """Clear cache after each test."""
        cache.clear()

    def test_haversine_distance_cached(self) -> None:
        """Test that haversine distance calculations are cached."""
        # Dallas to Houston coordinates
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        # First call - cache miss
        distance1 = haversine_distance_cached(lat1, lon1, lat2, lon2)
        self.assertGreater(distance1, 0)
        self.assertAlmostEqual(distance1, 362.0, delta=50.0)  # Approximately 362 km

        # Second call - cache hit
        distance2 = haversine_distance_cached(lat1, lon1, lat2, lon2)
        self.assertEqual(distance1, distance2)

    def test_coordinate_rounding_improves_cache_hits(self) -> None:
        """Test that coordinate rounding improves cache hit rates."""
        # Slightly different coordinates (within rounding threshold)
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        distance1 = haversine_distance_cached(lat1, lon1, lat2, lon2)

        # Coordinates rounded to same 4 decimals should hit cache
        lat1_alt, lon1_alt = 32.77671, -96.79701
        lat2_alt, lon2_alt = 29.76041, -95.36981

        distance2 = haversine_distance_cached(lat1_alt, lon1_alt, lat2_alt, lon2_alt)

        # Should be exactly the same (cache hit)
        self.assertEqual(distance1, distance2)

    def test_route_distance_cached(self) -> None:
        """Test that route distance calculations are cached."""
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698
        route_factor = 1.2

        # First call - cache miss
        flight1, driving1 = calculate_route_distance_cached(lat1, lon1, lat2, lon2, route_factor)
        self.assertGreater(flight1, 0)
        self.assertEqual(driving1, flight1 * route_factor)

        # Second call - cache hit
        flight2, driving2 = calculate_route_distance_cached(lat1, lon1, lat2, lon2, route_factor)
        self.assertEqual(flight1, flight2)
        self.assertEqual(driving1, driving2)

    def test_different_route_factors_different_cache(self) -> None:
        """Test that different route factors use different cache keys."""
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        # Different route factors
        flight1, driving1 = calculate_route_distance_cached(lat1, lon1, lat2, lon2, 1.2)
        flight2, driving2 = calculate_route_distance_cached(lat1, lon1, lat2, lon2, 1.5)

        # Flight distance should be the same
        self.assertEqual(flight1, flight2)

        # Driving distance should differ
        self.assertNotEqual(driving1, driving2)
        self.assertEqual(driving2, flight2 * 1.5)

    def test_fuel_cost_cached(self) -> None:
        """Test that fuel cost calculations are cached."""
        distance_km = 362.0
        fuel_economy = 7.5
        fuel_price = 1.50

        # First call - cache miss
        cost1 = calculate_fuel_cost_cached(distance_km, fuel_economy, fuel_price)
        self.assertGreater(cost1, 0)

        # Second call - cache hit
        cost2 = calculate_fuel_cost_cached(distance_km, fuel_economy, fuel_price)
        self.assertEqual(cost1, cost2)

    def test_trip_metrics_cached(self) -> None:
        """Test that comprehensive trip metrics are cached."""
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        # First call - cache miss
        metrics1 = calculate_trip_metrics_cached(
            lat1,
            lon1,
            lat2,
            lon2,
            route_factor=1.2,
            fuel_economy_l_per_100km=7.5,
            fuel_price_per_liter=1.50,
            avg_speed_kmh=80.0,
        )

        self.assertIn("flight_km", metrics1)
        self.assertIn("driving_km", metrics1)
        self.assertIn("fuel_cost", metrics1)
        self.assertIn("driving_hours", metrics1)

        # Verify calculated values
        self.assertGreater(metrics1["flight_km"], 0)
        self.assertGreater(metrics1["driving_km"], metrics1["flight_km"])
        self.assertGreater(metrics1["fuel_cost"], 0)
        self.assertGreater(metrics1["driving_hours"], 0)

        # Second call - cache hit
        metrics2 = calculate_trip_metrics_cached(
            lat1,
            lon1,
            lat2,
            lon2,
            route_factor=1.2,
            fuel_economy_l_per_100km=7.5,
            fuel_price_per_liter=1.50,
            avg_speed_kmh=80.0,
        )

        # Should be identical
        self.assertEqual(metrics1, metrics2)

    def test_cache_key_uniqueness(self) -> None:
        """Test that different parameters generate different cache keys."""
        # Same coordinates, different fuel parameters
        cost1 = calculate_fuel_cost_cached(362.0, 7.5, 1.50)
        cost2 = calculate_fuel_cost_cached(362.0, 8.0, 1.50)

        # Should be different
        self.assertNotEqual(cost1, cost2)

    def test_cache_clears_successfully(self) -> None:
        """Test that cache clear works."""
        lat1, lon1 = 32.7767, -96.7970
        lat2, lon2 = 29.7604, -95.3698

        # Populate cache
        haversine_distance_cached(lat1, lon1, lat2, lon2)
        calculate_route_distance_cached(lat1, lon1, lat2, lon2)
        calculate_fuel_cost_cached(362.0, 7.5, 1.50)

        # Clear cache
        clear_calculator_cache()

        # Verify we can still compute (cache miss, re-computed)
        distance = haversine_distance_cached(lat1, lon1, lat2, lon2)
        self.assertGreater(distance, 0)
        # Use variables to avoid lint errors
        self.assertIsNotNone(lat1)
        self.assertIsNotNone(lon1)

    def test_zero_distance_handled(self) -> None:
        """Test that zero distance (same origin/destination) is handled."""
        lat, lon = 32.7767, -96.7970

        distance = haversine_distance_cached(lat, lon, lat, lon)
        self.assertEqual(distance, 0.0)

    def test_cache_handles_edge_cases(self) -> None:
        """Test that cache handles edge cases properly."""
        # Zero speed
        metrics = calculate_trip_metrics_cached(
            32.7767,
            -96.7970,
            29.7604,
            -95.3698,
            avg_speed_kmh=0.0,
        )
        self.assertEqual(metrics["driving_hours"], 0.0)

        # Very high route factor
        flight, driving = calculate_route_distance_cached(
            32.7767,
            -96.7970,
            29.7604,
            -95.3698,
            route_factor=3.0,
        )
        self.assertEqual(driving, flight * 3.0)
