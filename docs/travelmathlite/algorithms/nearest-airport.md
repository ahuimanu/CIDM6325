# Nearest Airport Lookup: Bounding Box + Haversine

This note explains how TravelMathLite computes the nearest airports for a given coordinate without PostGIS, aligning with ADR-1.0.3.

## Approach Overview

- Prefilter via a coarse geographic bounding box around the query point to limit DB candidates.
- Compute precise distances in Python using the Haversine formula for each candidate.
- Sort by distance and return the top N (default 3).

## Bounding Box Prefilter

Given a query `(lat, lon)` and a radius in kilometers `R_km`, we derive an approximate bounding box:

- Degrees per km (latitude): ~1° per 111 km
- Latitude delta: `dlat = R_km / 111`
- Longitude delta: `dlon = dlat / max(cos(lat in radians), 0.1)`

The query applies:

- `latitude_deg BETWEEN (lat - dlat) AND (lat + dlat)`
- `longitude_deg BETWEEN (lon - dlon) AND (lon + dlon)`

Default radius: `radius_km = 2000` (portable default for SQLite-first; tune per use case).

## Country Prefilter (iso_country)

To improve precision and performance, callers can include an ISO 3166-1 alpha-2 country code:

- `iso_country = 'US'` filters candidates to United States airports only.
- The queryset also supports normalized `country` FK when present.

This optional prefilter reduces cross-border candidates and speeds up lookups in dense regions.

## Distance Calculation (Haversine)

For each candidate airport `(lat2, lon2)`, compute great-circle distance to `(lat1, lon1)`:

```text
R = 6371.0  # km
Δφ = radians(lat2 - lat1)
Δλ = radians(lon2 - lon1)
a = sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2)
c = 2 · atan2(√a, √(1−a))
distance_km = R · c
```

Units: results always include `distance_km`; when requested, a `distance_mi` convenience value is attached using `mi = km × 0.621371`.

## Defaults and Outputs

- Limit: `limit = 3`
- Radius: `radius_km = 2000`
- Unit: `unit = 'km' | 'mi'` (affects the extra attached value; sorting is by km)

Returned list is ordered by `distance_km` ascending with distances attached to each instance.

## Example Query

Given a coordinate near El Paso, Texas:

```python
from apps.airports.models import Airport

lat, lon = 31.76, -106.49
results = Airport.objects.nearest(lat, lon, limit=3, iso_country="US")

for airport in results:
    print(f"{airport.name} ({airport.iata_code}): {airport.distance_km:.2f} km")

# Output (sample):
# El Paso International (ELP): 10.23 km
# Las Cruces Intl (LRU): 78.45 km
# Alamogordo-White Sands Regional (ALM): 135.67 km
```

The queryset attaches `distance_km` (and optionally `distance_mi`) to each instance for display.

## Performance and Indexes

**Target:** p95 < 300 ms on a 50k-airport dataset (typical for OurAirports).

**Why this works well on SQLite without PostGIS:**

- Bounding box filters use standard B-tree indexes on `(latitude_deg, longitude_deg)`, `iso_country`, and `active`.
- SQLite excels at these simple range queries; no GIS extensions needed.
- Python-side haversine computation is fast for candidate sets (typically < 100 airports after bbox filter).
- For larger datasets or sub-50ms requirements, consider PostGIS or spatial indexes.

**Index usage:**

- `latitude_deg, longitude_deg` composite index accelerates bbox filtering.
- `iso_country` index speeds up country prefilter when specified.
- `active` index ensures inactive airports are excluded early.

## Limitations

- **Accuracy:** Haversine assumes a spherical Earth; geodesic (WGS84 ellipsoid) is more accurate but requires `geopy` or similar. Current error: < 0.5% for distances < 1000 km.
- **Bounding box approximation:** Longitude delta uses `cos(lat)` heuristic; near poles (lat > 80°) results may be imprecise.
- **Cross-border:** Without `iso_country` filter, results may include airports from neighboring countries if they're closer.
- **Performance at scale:** For datasets > 100k airports or real-time queries at high volume, consider adding PostGIS and spatial indexes.

## References

- ADR: `docs/travelmathlite/adr/adr-1.0.3-nearest-airport-lookup-implementation.md`
- Implementation: `travelmathlite/apps/airports/models.py` (`AirportQuerySet.nearest`)
- Tests: `travelmathlite/apps/airports/tests_nearest_core.py`
- Django docs: <https://docs.djangoproject.com/>
