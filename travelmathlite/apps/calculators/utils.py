"""Caching utilities for distance and cost calculations.

Provides cached versions of expensive computational operations to improve performance.
"""

from __future__ import annotations

from django.core.cache import cache

from .geo import haversine_distance

# Cache TTL: 15 minutes (900 seconds)
CACHE_TTL = 900


def haversine_distance_cached(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate haversine distance with caching.

    Cache key pattern: travelmathlite:distance:haversine:{coords}

    Coordinates are rounded to 4 decimal places (~11m precision) to optimize
    cache hit rates while maintaining reasonable accuracy.

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees

    Returns:
        Distance in kilometers
    """
    # Round coordinates to 4 decimal places for cache key
    # This provides ~11 meter precision which is sufficient for most use cases
    # and significantly improves cache hit rates
    coords = f"{round(lat1, 4)}:{round(lon1, 4)}:{round(lat2, 4)}:{round(lon2, 4)}"
    cache_key = f"travelmathlite:distance:haversine:{coords}"

    # Try cache first
    distance = cache.get(cache_key)
    if distance is not None:
        return distance

    # Cache miss - compute distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)

    # Store in cache
    cache.set(cache_key, distance, CACHE_TTL)

    return distance


def calculate_route_distance_cached(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    route_factor: float = 1.2,
) -> tuple[float, float]:
    """Calculate flight and estimated driving distance with caching.

    Cache key pattern: travelmathlite:distance:route:{coords}:{route_factor}

    Args:
        lat1: Origin latitude
        lon1: Origin longitude
        lat2: Destination latitude
        lon2: Destination longitude
        route_factor: Multiplier for driving distance (default 1.2 = 20% longer)

    Returns:
        Tuple of (flight_distance_km, driving_distance_km)
    """
    # Round coordinates and route factor for cache key
    coords = f"{round(lat1, 4)}:{round(lon1, 4)}:{round(lat2, 4)}:{round(lon2, 4)}:{round(route_factor, 2)}"
    cache_key = f"travelmathlite:distance:route:{coords}"

    def compute_distances() -> tuple[float, float]:
        flight_distance = haversine_distance(lat1, lon1, lat2, lon2)
        driving_distance = flight_distance * route_factor
        return (flight_distance, driving_distance)

    result = cache.get_or_set(cache_key, compute_distances, CACHE_TTL)
    return result if result is not None else (0.0, 0.0)


def calculate_fuel_cost_cached(
    distance_km: float,
    fuel_economy_l_per_100km: float,
    fuel_price_per_liter: float,
) -> float:
    """Calculate fuel cost for a trip with caching.

    Cache key pattern: travelmathlite:cost:fuel:{params}

    Args:
        distance_km: Distance in kilometers
        fuel_economy_l_per_100km: Fuel consumption (liters per 100km)
        fuel_price_per_liter: Fuel price per liter

    Returns:
        Total fuel cost
    """
    # Round values for cache key
    params = f"{round(distance_km, 1)}:{round(fuel_economy_l_per_100km, 1)}:{round(fuel_price_per_liter, 2)}"
    cache_key = f"travelmathlite:cost:fuel:{params}"

    def compute_cost() -> float:
        # Import here to avoid circular dependency
        from .costs import calculate_fuel_cost

        return calculate_fuel_cost(distance_km, fuel_economy_l_per_100km, fuel_price_per_liter)

    result = cache.get_or_set(cache_key, compute_cost, CACHE_TTL)
    return result if result is not None else 0.0


def calculate_trip_metrics_cached(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    route_factor: float = 1.2,
    fuel_economy_l_per_100km: float = 7.5,
    fuel_price_per_liter: float = 1.50,
    avg_speed_kmh: float = 80.0,
) -> dict[str, float]:
    """Calculate comprehensive trip metrics with caching.

    Cache key pattern: travelmathlite:trip:metrics:{coords}:{params}

    Args:
        lat1: Origin latitude
        lon1: Origin longitude
        lat2: Destination latitude
        lon2: Destination longitude
        route_factor: Driving distance multiplier
        fuel_economy_l_per_100km: Fuel consumption
        fuel_price_per_liter: Fuel price
        avg_speed_kmh: Average driving speed

    Returns:
        Dict with keys: flight_km, driving_km, fuel_cost, driving_hours
    """
    # Create cache key from all parameters
    coords_key = f"{round(lat1, 4)}:{round(lon1, 4)}:{round(lat2, 4)}:{round(lon2, 4)}"
    params_key = f"{round(route_factor, 2)}:{round(fuel_economy_l_per_100km, 1)}:{round(fuel_price_per_liter, 2)}:{round(avg_speed_kmh, 0)}"
    cache_key = f"travelmathlite:trip:metrics:{coords_key}:{params_key}"

    def compute_metrics() -> dict[str, float]:
        from .costs import calculate_fuel_cost

        # Calculate distances
        flight_km = haversine_distance(lat1, lon1, lat2, lon2)
        driving_km = flight_km * route_factor

        # Calculate cost
        fuel_cost = calculate_fuel_cost(driving_km, fuel_economy_l_per_100km, fuel_price_per_liter)

        # Calculate time
        driving_hours = driving_km / avg_speed_kmh if avg_speed_kmh > 0 else 0.0

        return {
            "flight_km": flight_km,
            "driving_km": driving_km,
            "fuel_cost": fuel_cost,
            "driving_hours": driving_hours,
        }

    result = cache.get_or_set(cache_key, compute_metrics, CACHE_TTL)
    return result if result is not None else {"flight_km": 0.0, "driving_km": 0.0, "fuel_cost": 0.0, "driving_hours": 0.0}


def clear_calculator_cache(pattern: str | None = None) -> None:
    """Clear calculator-related cache entries.

    Args:
        pattern: Optional specific pattern to clear (e.g., 'distance:*').
                If None, clears all calculator cache keys.

    Note:
        This is a simple implementation. For production with many keys,
        consider using cache key versioning or Redis SCAN/DELETE pattern.
    """
    if pattern:
        cache_pattern = f"travelmathlite:{pattern}"
    else:
        cache_pattern = "travelmathlite:distance:*"

    # Try to use delete_pattern if available (Redis backend)
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern(cache_pattern)  # type: ignore[attr-defined]
        # Also clear other calculator patterns
        cache.delete_pattern("travelmathlite:cost:*")  # type: ignore[attr-defined]
        cache.delete_pattern("travelmathlite:trip:*")  # type: ignore[attr-defined]
    else:
        # Fallback: clear entire cache (not ideal for production)
        pass
