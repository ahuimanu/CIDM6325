"""Unit tests for cost calculation functions.

Tests fuel cost calculations, unit conversions, and edge cases
with boundary values and error handling.
"""

from django.test import TestCase, override_settings

from ..costs import (
    calculate_fuel_cost,
    gallons_to_liters,
    l_per_100km_to_mpg,
    liters_to_gallons,
    mpg_to_l_per_100km,
)


class FuelCostCalculationTests(TestCase):
    """Test fuel cost calculations."""

    def test_basic_calculation(self):
        """Test basic fuel cost with known values."""
        # 100 km, 8 L/100km, $1.50/L = $12.00
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 12.00)

    def test_zero_distance(self):
        """Test that zero distance results in zero cost."""
        cost = calculate_fuel_cost(distance_km=0.0, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 0.0)

    def test_long_distance(self):
        """Test calculation for long distance trip."""
        # 1000 km, 10 L/100km, $1.40/L = $140.00
        cost = calculate_fuel_cost(distance_km=1000.0, fuel_economy_l_per_100km=10.0, fuel_price_per_liter=1.40)
        self.assertEqual(cost, 140.00)

    def test_efficient_vehicle(self):
        """Test calculation with very efficient vehicle (low L/100km)."""
        # 100 km, 4 L/100km, $1.50/L = $6.00
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=4.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 6.00)

    def test_inefficient_vehicle(self):
        """Test calculation with inefficient vehicle (high L/100km)."""
        # 100 km, 15 L/100km, $1.50/L = $22.50
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=15.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 22.50)

    def test_rounding_to_cents(self):
        """Test that cost is properly rounded to 2 decimal places."""
        # Result should be rounded to nearest cent
        cost = calculate_fuel_cost(distance_km=123.45, fuel_economy_l_per_100km=8.765, fuel_price_per_liter=1.234)
        # Should be rounded to 2 decimal places
        self.assertEqual(len(str(cost).split(".")[-1]), 2)

    def test_no_rounding(self):
        """Test calculation without rounding."""
        cost = calculate_fuel_cost(
            distance_km=100.0,
            fuel_economy_l_per_100km=8.0,
            fuel_price_per_liter=1.50,
            round_to_cents=False,
        )
        # Exact calculation: 100/100 * 8 * 1.50 = 12.0
        self.assertEqual(cost, 12.0)

    @override_settings(FUEL_ECONOMY_L_PER_100KM=7.0, FUEL_PRICE_PER_LITER=1.60)
    def test_uses_settings_defaults(self):
        """Test that function uses settings defaults when params not provided."""
        # 100 km with defaults from settings: 7.0 L/100km, $1.60/L = $11.20
        cost = calculate_fuel_cost(distance_km=100.0)
        self.assertEqual(cost, 11.20)

    def test_negative_distance_raises_error(self):
        """Test that negative distance raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            calculate_fuel_cost(distance_km=-100.0, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50)
        self.assertIn("distance_km must be >= 0", str(cm.exception))

    def test_very_small_distance(self):
        """Test calculation for very small distance."""
        # 0.1 km, 8 L/100km, $1.50/L = $0.01
        cost = calculate_fuel_cost(distance_km=0.1, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50)
        self.assertAlmostEqual(cost, 0.01, places=2)

    def test_high_fuel_price(self):
        """Test calculation with high fuel price."""
        # 100 km, 8 L/100km, $5.00/L = $40.00
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=5.00)
        self.assertEqual(cost, 40.00)


class FuelEconomyConversionTests(TestCase):
    """Test fuel economy unit conversions between MPG and L/100km."""

    def test_mpg_to_l_per_100km(self):
        """Test MPG to L/100km conversion."""
        # 30 MPG ≈ 7.84 L/100km
        result = mpg_to_l_per_100km(30.0)
        self.assertAlmostEqual(result, 7.84, places=2)

    def test_l_per_100km_to_mpg(self):
        """Test L/100km to MPG conversion."""
        # 8 L/100km ≈ 29.4 MPG
        result = l_per_100km_to_mpg(8.0)
        self.assertAlmostEqual(result, 29.4, places=1)

    def test_round_trip_mpg_conversion(self):
        """Test converting MPG -> L/100km -> MPG returns original."""
        original_mpg = 25.0
        l_per_100km = mpg_to_l_per_100km(original_mpg)
        back_to_mpg = l_per_100km_to_mpg(l_per_100km)
        self.assertAlmostEqual(original_mpg, back_to_mpg, places=10)

    def test_high_mpg(self):
        """Test conversion for highly efficient vehicle."""
        # 50 MPG ≈ 4.7 L/100km
        result = mpg_to_l_per_100km(50.0)
        self.assertLess(result, 5.0)

    def test_low_mpg(self):
        """Test conversion for inefficient vehicle."""
        # 15 MPG ≈ 15.68 L/100km
        result = mpg_to_l_per_100km(15.0)
        self.assertGreater(result, 15.0)

    def test_mpg_zero_raises_error(self):
        """Test that zero MPG raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            mpg_to_l_per_100km(0.0)
        self.assertIn("MPG must be > 0", str(cm.exception))

    def test_mpg_negative_raises_error(self):
        """Test that negative MPG raises ValueError."""
        with self.assertRaises(ValueError):
            mpg_to_l_per_100km(-25.0)

    def test_l_per_100km_zero_raises_error(self):
        """Test that zero L/100km raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            l_per_100km_to_mpg(0.0)
        self.assertIn("L/100km must be > 0", str(cm.exception))

    def test_l_per_100km_negative_raises_error(self):
        """Test that negative L/100km raises ValueError."""
        with self.assertRaises(ValueError):
            l_per_100km_to_mpg(-8.0)


class VolumeConversionTests(TestCase):
    """Test volume conversions between gallons and liters."""

    def test_gallons_to_liters(self):
        """Test US gallons to liters conversion."""
        # 1 gallon = 3.78541 liters
        self.assertAlmostEqual(gallons_to_liters(1.0), 3.78541, places=5)
        self.assertAlmostEqual(gallons_to_liters(10.0), 37.8541, places=4)

    def test_liters_to_gallons(self):
        """Test liters to US gallons conversion."""
        # 3.78541 liters = 1 gallon
        self.assertAlmostEqual(liters_to_gallons(3.78541), 1.0, places=5)
        self.assertAlmostEqual(liters_to_gallons(10.0), 2.64172, places=5)

    def test_zero_volume(self):
        """Test zero volume conversions."""
        self.assertEqual(gallons_to_liters(0.0), 0.0)
        self.assertEqual(liters_to_gallons(0.0), 0.0)

    def test_round_trip_volume_conversion(self):
        """Test converting gallons -> liters -> gallons returns original."""
        original_gallons = 5.0
        liters = gallons_to_liters(original_gallons)
        back_to_gallons = liters_to_gallons(liters)
        self.assertAlmostEqual(original_gallons, back_to_gallons, places=10)

    def test_negative_gallons_raises_error(self):
        """Test that negative gallons raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            gallons_to_liters(-5.0)
        self.assertIn("Gallons must be >= 0", str(cm.exception))

    def test_negative_liters_raises_error(self):
        """Test that negative liters raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            liters_to_gallons(-10.0)
        self.assertIn("Liters must be >= 0", str(cm.exception))

    def test_large_volume(self):
        """Test conversion for large volumes."""
        # 1000 gallons to liters
        result = gallons_to_liters(1000.0)
        self.assertAlmostEqual(result, 3785.41, places=2)


class BoundaryValueTests(TestCase):
    """Test boundary values and edge cases."""

    def test_minimal_distance(self):
        """Test calculation with minimal positive distance."""
        # Very small distance - use 0.1 km instead and disable rounding
        cost = calculate_fuel_cost(distance_km=0.1, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50, round_to_cents=False)
        self.assertGreater(cost, 0)
        self.assertLess(cost, 0.02)

    def test_very_high_fuel_economy(self):
        """Test calculation with very high fuel consumption."""
        # 100 km, 50 L/100km (heavy truck), $1.50/L = $75.00
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=50.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 75.00)

    def test_very_low_fuel_economy(self):
        """Test calculation with very low fuel consumption (very efficient)."""
        # 100 km, 2 L/100km (hybrid), $1.50/L = $3.00
        cost = calculate_fuel_cost(distance_km=100.0, fuel_economy_l_per_100km=2.0, fuel_price_per_liter=1.50)
        self.assertEqual(cost, 3.00)

    def test_fractional_values(self):
        """Test calculation with fractional values."""
        cost = calculate_fuel_cost(distance_km=123.456, fuel_economy_l_per_100km=7.89, fuel_price_per_liter=1.23)
        # Should return a properly rounded value
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
