from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from apps.airports.models import Airport

from .costs import (
    calculate_fuel_cost,
    gallons_to_liters,
    l_per_100km_to_mpg,
    liters_to_gallons,
    mpg_to_l_per_100km,
)
from .forms import CostCalculatorForm, DistanceCalculatorForm
from .geo import (
    calculate_distance_between_points,
    estimate_driving_distance,
    geodesic_distance,
    haversine_distance,
    km_to_miles,
    miles_to_km,
)


class CalculatorsURLsAndTemplatesTests(TestCase):
    def test_reverse_index(self) -> None:
        self.assertEqual(reverse("calculators:index"), "/calculators/")

    def test_index_renders_with_partial(self) -> None:
        url = reverse("calculators:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/index.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "This is the Calculators app partial include.")


class UnitConversionTests(TestCase):
    """Test unit conversion functions for mathematical correctness."""

    def test_km_to_miles_conversion(self) -> None:
        """Test kilometer to miles conversion."""
        self.assertAlmostEqual(km_to_miles(100), 62.1371, places=4)
        self.assertAlmostEqual(km_to_miles(1), 0.621371, places=6)
        self.assertEqual(km_to_miles(0), 0.0)

    def test_miles_to_km_conversion(self) -> None:
        """Test miles to kilometers conversion."""
        self.assertAlmostEqual(miles_to_km(100), 160.934, places=3)
        self.assertAlmostEqual(miles_to_km(1), 1.60934, places=5)
        self.assertEqual(miles_to_km(0), 0.0)

    def test_round_trip_conversion(self) -> None:
        """Test that converting km -> miles -> km returns original value."""
        original_km = 100.0
        converted_miles = km_to_miles(original_km)
        back_to_km = miles_to_km(converted_miles)
        self.assertAlmostEqual(back_to_km, original_km, places=3)

    def test_reverse_round_trip_conversion(self) -> None:
        """Test that converting miles -> km -> miles returns original value."""
        original_miles = 100.0
        converted_km = miles_to_km(original_miles)
        back_to_miles = km_to_miles(converted_km)
        self.assertAlmostEqual(back_to_miles, original_miles, places=3)


class HaversineDistanceTests(TestCase):
    """Test haversine distance calculations with known city pairs."""

    def test_nyc_to_la_distance(self) -> None:
        """Test New York to Los Angeles distance (~3944 km)."""
        # NYC: 40.7128° N, 74.0060° W
        # LA: 34.0522° N, 118.2437° W
        distance = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        # Expected distance is approximately 3944 km
        self.assertGreater(distance, 3900)
        self.assertLess(distance, 4000)

    def test_london_to_paris_distance(self) -> None:
        """Test London to Paris distance (~344 km)."""
        # London: 51.5074° N, 0.1278° W
        # Paris: 48.8566° N, 2.3522° E
        distance = haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        # Expected distance is approximately 344 km
        self.assertGreater(distance, 340)
        self.assertLess(distance, 350)

    def test_same_point_distance(self) -> None:
        """Test that distance from a point to itself is zero."""
        distance = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 0.0, places=10)

    def test_short_distance(self) -> None:
        """Test a short distance (within same city)."""
        # Two points in Manhattan, approximately 1 km apart
        distance = haversine_distance(40.7589, -73.9851, 40.7489, -73.9680)
        self.assertGreater(distance, 0.5)
        self.assertLess(distance, 2.0)

    def test_antipodal_points(self) -> None:
        """Test distance between antipodal points (opposite sides of Earth)."""
        # North Pole to South Pole
        distance = haversine_distance(90, 0, -90, 0)
        # Expected distance is approximately half Earth's circumference (~20,000 km)
        self.assertGreater(distance, 19000)
        self.assertLess(distance, 21000)


class GeodesicDistanceTests(TestCase):
    """Test geodesic distance calculations (uses geopy if available, falls back to haversine)."""

    def test_geodesic_nyc_to_la(self) -> None:
        """Test geodesic distance from NYC to LA."""
        distance = geodesic_distance(40.7128, -74.0060, 34.0522, -118.2437)
        self.assertGreater(distance, 3900)
        self.assertLess(distance, 4000)

    def test_geodesic_london_to_paris(self) -> None:
        """Test geodesic distance from London to Paris."""
        distance = geodesic_distance(51.5074, -0.1278, 48.8566, 2.3522)
        self.assertGreater(distance, 340)
        self.assertLess(distance, 350)

    def test_geodesic_same_point(self) -> None:
        """Test geodesic distance from a point to itself is zero."""
        distance = geodesic_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 0.0, places=10)

    def test_geodesic_matches_haversine(self) -> None:
        """Test that geodesic and haversine give similar results for moderate distances."""
        lat1, lon1 = 51.5074, -0.1278
        lat2, lon2 = 48.8566, 2.3522
        geodesic = geodesic_distance(lat1, lon1, lat2, lon2)
        haversine = haversine_distance(lat1, lon1, lat2, lon2)
        # Should be within 1% of each other
        difference = abs(geodesic - haversine)
        self.assertLess(difference, geodesic * 0.01)


class DrivingDistanceEstimateTests(TestCase):
    """Test driving distance estimation with route factors."""

    def test_default_route_factor(self) -> None:
        """Test driving estimate with default route factor (1.2)."""
        straight_line = 100.0
        driving = estimate_driving_distance(straight_line)
        self.assertEqual(driving, 120.0)

    def test_custom_route_factor(self) -> None:
        """Test driving estimate with custom route factor."""
        straight_line = 100.0
        driving = estimate_driving_distance(straight_line, route_factor=1.3)
        self.assertEqual(driving, 130.0)

    def test_route_factor_of_one(self) -> None:
        """Test that route factor of 1.0 returns same as input."""
        straight_line = 100.0
        driving = estimate_driving_distance(straight_line, route_factor=1.0)
        self.assertEqual(driving, straight_line)

    def test_zero_distance(self) -> None:
        """Test driving estimate for zero distance."""
        driving = estimate_driving_distance(0.0)
        self.assertEqual(driving, 0.0)


class CalculateDistanceBetweenPointsTests(TestCase):
    """Test the main distance calculation function."""

    def test_calculate_distance_km_only(self) -> None:
        """Test distance calculation in kilometers without driving estimate."""
        flight, driving = calculate_distance_between_points(
            40.7128, -74.0060, 34.0522, -118.2437, unit="km", include_driving_estimate=False
        )
        self.assertGreater(flight, 3900)
        self.assertLess(flight, 4000)
        self.assertEqual(driving, 0.0)

    def test_calculate_distance_miles_only(self) -> None:
        """Test distance calculation in miles without driving estimate."""
        flight, driving = calculate_distance_between_points(
            40.7128, -74.0060, 34.0522, -118.2437, unit="miles", include_driving_estimate=False
        )
        # Approximately 2451 miles
        self.assertGreater(flight, 2400)
        self.assertLess(flight, 2500)
        self.assertEqual(driving, 0.0)

    def test_calculate_distance_with_driving_estimate_km(self) -> None:
        """Test distance with driving estimate in kilometers."""
        flight, driving = calculate_distance_between_points(
            40.7128,
            -74.0060,
            34.0522,
            -118.2437,
            unit="km",
            include_driving_estimate=True,
            route_factor=1.2,
        )
        self.assertGreater(flight, 3900)
        self.assertLess(flight, 4000)
        self.assertGreater(driving, flight)
        # Driving should be approximately 1.2x flight distance
        self.assertAlmostEqual(driving / flight, 1.2, places=10)

    def test_calculate_distance_with_driving_estimate_miles(self) -> None:
        """Test distance with driving estimate in miles."""
        flight, driving = calculate_distance_between_points(
            40.7128,
            -74.0060,
            34.0522,
            -118.2437,
            unit="miles",
            include_driving_estimate=True,
            route_factor=1.2,
        )
        self.assertGreater(flight, 2400)
        self.assertLess(flight, 2500)
        self.assertGreater(driving, flight)
        # Driving should be approximately 1.2x flight distance
        self.assertAlmostEqual(driving / flight, 1.2, places=10)

    def test_calculate_distance_custom_route_factor(self) -> None:
        """Test distance calculation with custom route factor."""
        flight, driving = calculate_distance_between_points(
            51.5074,
            -0.1278,
            48.8566,
            2.3522,
            unit="km",
            include_driving_estimate=True,
            route_factor=1.5,
        )
        self.assertAlmostEqual(driving / flight, 1.5, places=10)


class FormsValidationTests(TestCase):
    def setUp(self) -> None:
        # Minimal airport records for lookups
        Airport.objects.create(
            ident="KJFK",
            iata_code="JFK",
            name="John F. Kennedy International",
            airport_type="large_airport",
            latitude_deg=40.6413,
            longitude_deg=-73.7781,
            iso_country="US",
            municipality="new york",
        )
        Airport.objects.create(
            ident="LFPG",
            iata_code="CDG",
            name="Charles de Gaulle International",
            airport_type="large_airport",
            latitude_deg=49.0097,
            longitude_deg=2.5479,
            iso_country="FR",
            municipality="paris",
        )

    def test_direct_coordinates_parsing(self) -> None:
        form = DistanceCalculatorForm(
            data={
                "origin": "40.7128,-74.0060",
                "destination": "34.0522,-118.2437",
                "unit": "km",
                "route_factor": settings.ROUTE_FACTOR,
            }
        )
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertAlmostEqual(form.origin_coords[0], 40.7128, places=4)
        self.assertAlmostEqual(form.origin_coords[1], -74.0060, places=4)

    def test_iata_code_lookup(self) -> None:
        form = DistanceCalculatorForm(
            data={
                "origin": "JFK",
                "destination": "40.7128,-74.0060",
                "unit": "miles",
                "route_factor": settings.ROUTE_FACTOR,
            }
        )
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertAlmostEqual(form.origin_coords[0], 40.6413, places=3)
        self.assertAlmostEqual(form.origin_coords[1], -73.7781, places=3)

    def test_city_lookup_via_airports_municipality(self) -> None:
        form = DistanceCalculatorForm(
            data={
                "origin": "paris",
                "destination": "london",
                "unit": "km",
                "route_factor": settings.ROUTE_FACTOR,
            }
        )
        # Destination 'london' not in airports.municipality test data but exists in fallback map
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertAlmostEqual(form.origin_coords[0], 49.0097, places=3)
        self.assertAlmostEqual(form.origin_coords[1], 2.5479, places=3)

    def test_invalid_coordinate_range(self) -> None:
        form = DistanceCalculatorForm(
            data={
                "origin": "200,10",
                "destination": "0,0",
                "unit": "km",
                "route_factor": settings.ROUTE_FACTOR,
            }
        )
        self.assertFalse(form.is_valid())

    def test_unknown_iata_rejected(self) -> None:
        form = DistanceCalculatorForm(
            data={
                "origin": "ZZZ",
                "destination": "0,0",
                "unit": "km",
                "route_factor": settings.ROUTE_FACTOR,
            }
        )
        self.assertFalse(form.is_valid())

    def test_defaults_populated_from_settings(self) -> None:
        form = DistanceCalculatorForm()
        self.assertAlmostEqual(form.fields["route_factor"].initial, settings.ROUTE_FACTOR)
        cost_form = CostCalculatorForm()
        self.assertAlmostEqual(cost_form.fields["fuel_economy_l_per_100km"].initial, settings.FUEL_ECONOMY_L_PER_100KM)
        self.assertAlmostEqual(cost_form.fields["fuel_price_per_liter"].initial, settings.FUEL_PRICE_PER_LITER)


class CostUnitConversionTests(TestCase):
    def test_mpg_to_l_per_100km_and_back(self) -> None:
        mpg = 30.0
        l_per_100 = mpg_to_l_per_100km(mpg)
        self.assertAlmostEqual(l_per_100, 235.214 / 30.0, places=6)
        back_to_mpg = l_per_100km_to_mpg(l_per_100)
        self.assertAlmostEqual(back_to_mpg, mpg, places=6)

    def test_gallons_to_liters_and_back(self) -> None:
        gallons = 10.0
        liters = gallons_to_liters(gallons)
        self.assertAlmostEqual(liters, 37.8541, places=4)
        back_to_gallons = liters_to_gallons(liters)
        self.assertAlmostEqual(back_to_gallons, gallons, places=6)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            mpg_to_l_per_100km(0)
        with self.assertRaises(ValueError):
            l_per_100km_to_mpg(0)
        with self.assertRaises(ValueError):
            gallons_to_liters(-1)
        with self.assertRaises(ValueError):
            liters_to_gallons(-1)


class CostCalculationTests(TestCase):
    def test_defaults_from_settings(self) -> None:
        # Using defaults: 100 km, 7.5 L/100km, 1.50 /L => 11.25
        cost = calculate_fuel_cost(100.0)
        self.assertEqual(cost, 11.25)

    def test_overrides(self) -> None:
        # 200 km, 8.0 L/100km, 2.00 /L => (200/100)*8*2 = 32.0
        cost = calculate_fuel_cost(200.0, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=2.0)
        self.assertEqual(cost, 32.0)

    def test_rounding(self) -> None:
        # Choose values that produce repeating decimals and ensure rounding
        cost = calculate_fuel_cost(123.0, fuel_economy_l_per_100km=7.7, fuel_price_per_liter=1.33)
        self.assertIsInstance(cost, float)
        # Compute expected manually
        expected = round((123.0 / 100.0) * 7.7 * 1.33, 2)
        self.assertEqual(cost, expected)

    def test_negative_distance_raises(self) -> None:
        with self.assertRaises(ValueError):
            calculate_fuel_cost(-1.0)


class SettingsDefaultsTests(TestCase):
    """Ensure calculator settings defaults are present and properly typed."""

    def test_settings_defaults_exist_and_types(self) -> None:
        self.assertTrue(hasattr(settings, "ROUTE_FACTOR"))
        self.assertTrue(hasattr(settings, "AVG_SPEED_KMH"))
        self.assertTrue(hasattr(settings, "FUEL_PRICE_PER_LITER"))
        self.assertTrue(hasattr(settings, "FUEL_ECONOMY_L_PER_100KM"))

        self.assertIsInstance(settings.ROUTE_FACTOR, float)
        self.assertIsInstance(settings.AVG_SPEED_KMH, float)
        self.assertIsInstance(settings.FUEL_PRICE_PER_LITER, float)
        self.assertIsInstance(settings.FUEL_ECONOMY_L_PER_100KM, float)

    def test_settings_default_values(self) -> None:
        # Defaults per ADR 1.0.2 brief
        self.assertAlmostEqual(settings.ROUTE_FACTOR, 1.2, places=6)
        self.assertAlmostEqual(settings.AVG_SPEED_KMH, 80.0, places=6)
        self.assertAlmostEqual(settings.FUEL_PRICE_PER_LITER, 1.50, places=6)
        self.assertAlmostEqual(settings.FUEL_ECONOMY_L_PER_100KM, 7.5, places=6)


class CalculatorsViewAndHTMXTests(TestCase):
    def setUp(self) -> None:
        # Seed minimal airports for lookups
        Airport.objects.create(
            ident="KJFK",
            iata_code="JFK",
            name="John F. Kennedy International",
            airport_type="large_airport",
            latitude_deg=40.6413,
            longitude_deg=-73.7781,
            iso_country="US",
            municipality="new york",
        )
        Airport.objects.create(
            ident="LFPG",
            iata_code="CDG",
            name="Charles de Gaulle International",
            airport_type="large_airport",
            latitude_deg=49.0097,
            longitude_deg=2.5479,
            iso_country="FR",
            municipality="paris",
        )

    def test_distance_view_get_renders(self) -> None:
        url = reverse("calculators:distance")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/distance_calculator.html")
        # Form should post to the partial endpoint via HTMX
        self.assertContains(resp, reverse("calculators:distance-partial"))

    def test_cost_view_get_renders(self) -> None:
        url = reverse("calculators:cost")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/cost_calculator.html")
        self.assertContains(resp, reverse("calculators:cost-partial"))

    def test_distance_partial_post_valid_htmx(self) -> None:
        url = reverse("calculators:distance-partial")
        data = {
            "origin": "JFK",
            "destination": "CDG",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/partials/distance_result.html")
        self.assertContains(resp, "Flight distance")

    def test_distance_partial_post_invalid_returns_400(self) -> None:
        url = reverse("calculators:distance-partial")
        data = {
            "origin": "ZZZ",  # invalid code given our seed data
            "destination": "not-a-place",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 400)
        # Should re-render the form page with errors
        self.assertTemplateUsed(resp, "calculators/distance_calculator.html")

    def test_cost_partial_post_valid_htmx(self) -> None:
        url = reverse("calculators:cost-partial")
        data = {
            "origin": "JFK",
            "destination": "CDG",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
            "fuel_economy_l_per_100km": settings.FUEL_ECONOMY_L_PER_100KM,
            "fuel_price_per_liter": settings.FUEL_PRICE_PER_LITER,
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/partials/cost_result.html")
        self.assertContains(resp, "Estimated fuel cost")

    def test_cost_partial_post_invalid_returns_400(self) -> None:
        url = reverse("calculators:cost-partial")
        data = {
            "origin": "bad-origin",
            "destination": "bad-dest",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
            "fuel_economy_l_per_100km": -1,  # invalid
            "fuel_price_per_liter": -1,  # invalid
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 400)
        self.assertTemplateUsed(resp, "calculators/cost_calculator.html")

    def test_distance_cbv_post_without_htmx_renders_full_page_with_results(self) -> None:
        url = reverse("calculators:distance")
        data = {
            "origin": "JFK",
            "destination": "CDG",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/distance_calculator.html")
        self.assertContains(resp, "Distance Calculator")
        # The page should include the partial content when valid
        self.assertContains(resp, "Flight distance")

    def test_cost_cbv_post_without_htmx_renders_full_page_with_results(self) -> None:
        url = reverse("calculators:cost")
        data = {
            "origin": "JFK",
            "destination": "CDG",
            "unit": "km",
            "route_factor": settings.ROUTE_FACTOR,
            "fuel_economy_l_per_100km": settings.FUEL_ECONOMY_L_PER_100KM,
            "fuel_price_per_liter": settings.FUEL_PRICE_PER_LITER,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/cost_calculator.html")
        self.assertContains(resp, "Trip Cost Calculator")
        self.assertContains(resp, "Estimated fuel cost")


class HTMXRequestDetectionTests(TestCase):
    """Test HTMX request detection and partial template rendering (ADR-1.0.5)."""

    def setUp(self) -> None:
        """Create test airports."""
        self.ama = Airport.objects.create(
            ident="KAMA",
            iata_code="AMA",
            name="Rick Husband Amarillo International Airport",
            municipality="Amarillo",
            latitude_deg=35.2194,
            longitude_deg=-101.7059,
            active=True,
        )
        self.dfw = Airport.objects.create(
            ident="KDFW",
            iata_code="DFW",
            name="Dallas Fort Worth International Airport",
            municipality="Dallas-Fort Worth",
            latitude_deg=32.8968,
            longitude_deg=-97.0380,
            active=True,
        )

    def test_distance_calculator_htmx_request_returns_partial(self) -> None:
        """HTMX requests to distance calculator should return partial template."""
        url = reverse("calculators:distance")
        data = {
            "origin": "AMA",  # Use IATA code as string
            "destination": "DFW",  # Use IATA code as string
            "unit": "km",
            "route_factor": "1.2",
        }
        # Simulate HTMX request with HX-Request header
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/partials/distance_result.html")
        self.assertTemplateNotUsed(resp, "calculators/distance_calculator.html")
        self.assertContains(resp, "Distance Results")
        self.assertContains(resp, "Flight distance")

    def test_distance_calculator_standard_request_returns_full_page(self) -> None:
        """Standard POST requests should return full page template."""
        url = reverse("calculators:distance")
        data = {
            "origin": "AMA",
            "destination": "DFW",
            "unit": "km",
            "route_factor": "1.2",
        }
        # Standard POST without HTMX header
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/distance_calculator.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "Distance Calculator")

    def test_distance_calculator_htmx_validation_error_returns_partial(self) -> None:
        """HTMX requests with validation errors should return partial with errors."""
        url = reverse("calculators:distance")
        data = {
            "origin": "",  # Missing origin
            "destination": "DFW",
            "unit": "km",
            "route_factor": "1.2",
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 400)  # Bad request
        self.assertTemplateUsed(resp, "calculators/partials/distance_result.html")
        self.assertContains(resp, "Please correct the following errors", status_code=400)

    def test_cost_calculator_htmx_request_returns_partial(self) -> None:
        """HTMX requests to cost calculator should return partial template."""
        url = reverse("calculators:cost")
        data = {
            "origin": "AMA",
            "destination": "DFW",
            "unit": "km",
            "route_factor": "1.2",
            "fuel_economy_l_per_100km": "8.0",
            "fuel_price_per_liter": "1.50",
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/partials/cost_result.html")
        self.assertTemplateNotUsed(resp, "calculators/cost_calculator.html")
        self.assertContains(resp, "Cost Estimate Results")
        self.assertContains(resp, "Estimated fuel cost")

    def test_cost_calculator_standard_request_returns_full_page(self) -> None:
        """Standard POST requests should return full page template."""
        url = reverse("calculators:cost")
        data = {
            "origin": "AMA",
            "destination": "DFW",
            "unit": "km",
            "route_factor": "1.2",
            "fuel_economy_l_per_100km": "8.0",
            "fuel_price_per_liter": "1.50",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "calculators/cost_calculator.html")
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "Trip Cost Calculator")

    def test_cost_calculator_htmx_validation_error_returns_partial(self) -> None:
        """HTMX requests with validation errors should return partial with errors."""
        url = reverse("calculators:cost")
        data = {
            "origin": "AMA",
            "destination": "",  # Missing destination
            "unit": "km",
            "route_factor": "1.2",
            "fuel_economy_l_per_100km": "8.0",
            "fuel_price_per_liter": "1.50",
        }
        resp = self.client.post(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 400)
        self.assertTemplateUsed(resp, "calculators/partials/cost_result.html")
        self.assertContains(resp, "Please correct the following errors", status_code=400)

    def test_csrf_token_present_in_full_page(self) -> None:
        """Full page templates should include CSRF token (INV-2)."""
        url = reverse("calculators:distance")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "csrfmiddlewaretoken")
