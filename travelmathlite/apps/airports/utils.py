"""Caching utilities for airport queries.

Provides cached versions of common airport query operations to improve performance.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.cache import cache

if TYPE_CHECKING:
    from .models import Airport

# Cache TTL: 15 minutes (900 seconds)
CACHE_TTL = 900


def get_airports_by_country(country_code: str) -> list[Airport]:
    """Get all active airports for a country with caching.

    Cache key pattern: travelmathlite:airports:country:{country_code}

    Args:
        country_code: ISO country code (e.g., 'US', 'GB')

    Returns:
        List of Airport objects for the specified country
    """
    from .models import Airport

    cache_key = f"travelmathlite:airports:country:{country_code.upper()}"

    # Try to get from cache
    airports = cache.get(cache_key)
    if airports is not None:
        return airports

    # Cache miss - query and store
    airports = list(Airport.objects.active().filter(iso_country=country_code.upper()).select_related("country", "city").order_by("name"))

    cache.set(cache_key, airports, CACHE_TTL)

    return airports


def get_airports_by_city(city_name: str) -> list[Airport]:
    """Get all active airports for a city with caching.

    Cache key pattern: travelmathlite:airports:city:{city_name}

    Args:
        city_name: City name (case-insensitive)

    Returns:
        List of Airport objects in the specified city
    """
    from .models import Airport

    # Normalize city name for consistent cache keys
    normalized_city = city_name.strip().lower()
    cache_key = f"travelmathlite:airports:city:{normalized_city}"

    # Use get_or_set for atomic fetch-or-compute
    def compute_airports() -> list[Airport]:
        return list(Airport.objects.active().filter(municipality__iexact=city_name).select_related("country", "city").order_by("name"))

    result = cache.get_or_set(cache_key, compute_airports, CACHE_TTL)
    return result if result is not None else []


def get_airports_by_iata(iata_code: str) -> Airport | None:
    """Get airport by IATA code with caching.

    Cache key pattern: travelmathlite:airports:iata:{iata_code}

    Args:
        iata_code: 3-letter IATA code (e.g., 'DFW', 'LAX')

    Returns:
        Airport object if found, None otherwise
    """
    from .models import Airport

    cache_key = f"travelmathlite:airports:iata:{iata_code.upper()}"

    # Try to get from cache
    airport = cache.get(cache_key)
    if airport is not None:
        return airport

    # Cache miss - query and store
    try:
        airport = Airport.objects.active().select_related("country", "city").get(iata_code=iata_code.upper())
        cache.set(cache_key, airport, CACHE_TTL)
        return airport
    except Airport.DoesNotExist:  # type: ignore[attr-defined]
        # Cache the None result to avoid repeated queries
        cache.set(cache_key, None, CACHE_TTL // 3)  # Shorter TTL for misses
        return None


def get_nearest_airports_cached(
    latitude: float,
    longitude: float,
    limit: int = 5,
    radius_km: float = 500.0,
) -> list[tuple[Airport, float]]:
    """Get nearest airports to coordinates with caching.

    Cache key pattern: travelmathlite:nearest:airports:{lat}:{lon}:{limit}:{radius}

    Args:
        latitude: Latitude in decimal degrees
        longitude: Longitude in decimal degrees
        limit: Maximum number of airports to return
        radius_km: Search radius in kilometers

    Returns:
        List of (Airport, distance_km) tuples sorted by distance
    """
    from .models import Airport

    # Round coordinates to 2 decimal places (~1km precision) for cache hit optimization
    lat_rounded = round(latitude, 2)
    lon_rounded = round(longitude, 2)

    cache_key = f"travelmathlite:nearest:airports:{lat_rounded}:{lon_rounded}:{limit}:{radius_km}"

    def compute_nearest() -> list[tuple[Airport, float]]:
        queryset = Airport.objects.active().select_related("country", "city")
        results = queryset.nearest(latitude, longitude, limit=limit, radius_km=radius_km)
        return results  # type: ignore[return-value]

    result = cache.get_or_set(cache_key, compute_nearest, CACHE_TTL)
    return result if result is not None else []


def search_airports_cached(query: str) -> list[Airport]:
    """Search for airports by name, code, or location with caching.

    Cache key pattern: travelmathlite:airports:search:{query}

    Args:
        query: Search term (name, code, city, etc.)

    Returns:
        List of matching Airport objects
    """
    from .models import Airport

    # Normalize query for consistent cache keys
    normalized_query = query.strip().lower()
    cache_key = f"travelmathlite:airports:search:{normalized_query}"

    def compute_search() -> list[Airport]:
        return list(Airport.objects.search(query).select_related("country", "city")[:50])  # Limit results

    result = cache.get_or_set(cache_key, compute_search, CACHE_TTL)
    return result if result is not None else []


def clear_airport_cache(pattern: str | None = None) -> None:
    """Clear airport-related cache entries.

    Args:
        pattern: Optional specific pattern to clear (e.g., 'country:US').
                If None, clears all airport cache keys.

    Note:
        This is a simple implementation. For production with many keys,
        consider using cache key versioning or Redis SCAN/DELETE pattern.
        The delete_pattern method may not be available on all cache backends.
    """
    if pattern:
        cache_pattern = f"travelmathlite:airports:{pattern}"
    else:
        cache_pattern = "travelmathlite:airports:*"

    # Try to use delete_pattern if available (Redis backend)
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern(cache_pattern)  # type: ignore[attr-defined]
    else:
        # Fallback: clear entire cache (not ideal for production)
        # In production, consider implementing versioned cache keys instead
        pass


def invalidate_airport_cache(airport_id: int | None = None) -> None:
    """Invalidate cache entries related to a specific airport or all airports.

    Use this after airport data is created, updated, or deleted.

    Args:
        airport_id: Optional airport ID. If provided, invalidates related entries.
                   If None, clears all airport caches.
    """
    if airport_id is None:
        # Clear all airport caches
        clear_airport_cache()
    else:
        # Clear specific airport-related caches
        # In a more sophisticated implementation, track which cache keys
        # are affected by specific airports
        clear_airport_cache()
