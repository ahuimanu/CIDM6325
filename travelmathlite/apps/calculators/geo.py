"""
Geodesic and distance calculation utilities.

This module provides functions for calculating distances between geographic
coordinates using haversine and geodesic formulas, unit conversions, and
heuristic driving distance estimates.
"""

import math

# Unit conversion constants
KM_TO_MILES_FACTOR = 0.621371
MILES_TO_KM_FACTOR = 1.60934
EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using the
    Haversine formula.

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees

    Returns:
        Distance in kilometers

    Examples:
        >>> # New York to Los Angeles (approximately 3944 km)
        >>> dist = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        >>> 3900 < dist < 4000
        True
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return EARTH_RADIUS_KM * c


def geodesic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the geodesic distance between two points on Earth.

    This implementation uses the Vincenty formula for better accuracy than
    Haversine, especially for antipodal points. Falls back to Haversine if
    geopy is not available.

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees

    Returns:
        Distance in kilometers

    Examples:
        >>> # London to Paris (approximately 344 km)
        >>> dist = geodesic_distance(51.5074, -0.1278, 48.8566, 2.3522)
        >>> 340 < dist < 350
        True
    """
    try:
        from geopy.distance import geodesic as geopy_geodesic  # type: ignore[import-untyped]

        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance = float(geopy_geodesic(point1, point2).kilometers)  # type: ignore[attr-defined]
        return distance
    except ImportError:
        # Fall back to haversine if geopy is not available
        return haversine_distance(lat1, lon1, lat2, lon2)


def km_to_miles(km: float) -> float:
    """
    Convert kilometers to miles.

    Args:
        km: Distance in kilometers

    Returns:
        Distance in miles

    Examples:
        >>> km_to_miles(100)
        62.1371
        >>> km_to_miles(0)
        0.0
    """
    return km * KM_TO_MILES_FACTOR


def miles_to_km(miles: float) -> float:
    """
    Convert miles to kilometers.

    Args:
        miles: Distance in miles

    Returns:
        Distance in kilometers

    Examples:
        >>> miles_to_km(100)
        160.934
        >>> miles_to_km(0)
        0.0
    """
    return miles * MILES_TO_KM_FACTOR


def estimate_driving_distance(straight_line_km: float, route_factor: float = 1.2) -> float:
    """
    Estimate driving distance from straight-line distance using a route factor.

    The route factor accounts for the fact that roads are not straight lines.
    A typical route factor is 1.2, meaning driving distance is approximately
    20% longer than straight-line distance.

    Args:
        straight_line_km: Straight-line distance in kilometers
        route_factor: Multiplier for route deviation (default: 1.2)

    Returns:
        Estimated driving distance in kilometers

    Examples:
        >>> estimate_driving_distance(100)
        120.0
        >>> estimate_driving_distance(100, route_factor=1.3)
        130.0
    """
    return straight_line_km * route_factor


def calculate_distance_between_points(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = "km",
    include_driving_estimate: bool = False,
    route_factor: float = 1.2,
) -> tuple[float, float]:
    """
    Calculate distance between two points with optional driving estimate.

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees
        unit: Output unit ('km' or 'miles', default: 'km')
        include_driving_estimate: Whether to include driving distance estimate
        route_factor: Route factor for driving estimate (default: 1.2)

    Returns:
        Tuple of (straight_line_distance, driving_distance_estimate)
        If include_driving_estimate is False, driving_distance_estimate is 0.0

    Examples:
        >>> flight, driving = calculate_distance_between_points(
        ...     40.7128, -74.0060, 34.0522, -118.2437,
        ...     unit='km', include_driving_estimate=True
        ... )
        >>> 3900 < flight < 4000
        True
        >>> driving > flight
        True
    """
    # Calculate geodesic distance
    distance_km = geodesic_distance(lat1, lon1, lat2, lon2)

    # Convert to requested unit
    if unit.lower() == "miles":
        straight_line = km_to_miles(distance_km)
    else:
        straight_line = distance_km

    # Calculate driving estimate if requested
    if include_driving_estimate:
        driving_km = estimate_driving_distance(distance_km, route_factor)
        driving = km_to_miles(driving_km) if unit.lower() == "miles" else driving_km
        return straight_line, driving
    else:
        return straight_line, 0.0
