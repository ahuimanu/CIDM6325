# Distance, Time, and Cost Calculations

This document explains how TravelMathLite computes distances, estimated driving time, and estimated fuel cost for trips. It also lists defaults, unit conversions, examples, and limitations so both developers and non-technical readers can understand assumptions and outputs.

## Distance calculations

- Straight-line ("as-the-crow-flies") distance between two coordinates uses either the geodesic distance (via `geopy`, when available) or a Haversine fallback.
- Haversine formula (spherical Earth approximation):
  - Given coordinates (lat1, lon1) and (lat2, lon2) in radians and Earth radius R=6,371 km,
  - d = 2R × atan2( sqrt(a), sqrt(1−a) ), where a = sin²(Δφ/2) + cos φ1 × cos φ2 × sin²(Δλ/2)
- Estimated driving distance uses a heuristic multiplier instead of real turn-by-turn routing:
  - driving_distance_km = straight_line_km × route_factor
  - Default route_factor = 1.2 (accounts for road curvature, detours, and typical routing overhead)

## Time calculations

- Estimated driving time in hours uses an average speed assumption:
  - driving_time_hours = driving_distance_km / avg_speed_kmh
  - Default avg_speed_kmh = 80.0 (mixed highway/urban conditions)

## Cost calculations

- Fuel cost uses distance in kilometers, vehicle fuel economy in L/100km, and fuel price per liter:
  - fuel_cost = (distance_km / 100) × fuel_economy_l_per_100km × fuel_price_per_liter
- Defaults:
  - fuel_economy_l_per_100km = 7.5
  - fuel_price_per_liter = 1.50 (currency-agnostic; shown as /L)

## Unit conversions

- Kilometers ↔ miles:
  - 1 mile = 1.60934 kilometers
  - km = miles × 1.60934
  - miles = km ÷ 1.60934
- MPG ↔ L/100km:
  - L/100km = 235.214 ÷ MPG
  - MPG = 235.214 ÷ (L/100km)
- Gallons ↔ liters:
  - 1 gallon = 3.78541 liters
  - liters = gallons × 3.78541
  - gallons = liters ÷ 3.78541

## Worked example

- Route: New York City (NYC) to Los Angeles (LA)
- Straight-line distance ≈ 3,944 km
- Driving distance (heuristic): 3,944 × 1.2 ≈ 4,733 km
- Driving time at 80 km/h: 4,733 ÷ 80 ≈ 59.16 hours
- Fuel cost with defaults (7.5 L/100km, 1.50 /L):
  - (4,733 / 100) × 7.5 × 1.50 ≈ 532.46

Note: Values are approximate and rounded for readability.

## Defaults and configuration

- The following defaults are used unless overridden via settings or form inputs:
  - route_factor: 1.2
  - avg_speed_kmh: 80.0
  - fuel_economy_l_per_100km: 7.5
  - fuel_price_per_liter: 1.50

## Limitations and assumptions

- No real-time routing: driving distance is an estimate based on a route factor, not actual road networks or traffic.
- Average conditions: speed and economy assumptions are generic; actual times and costs vary based on route, vehicle, terrain, weather, and driving style.
- Geodesic vs. Haversine: when geodesic libraries are unavailable, the spherical approximation is used and remains sufficiently accurate for typical use.

## Related

- PRD §4: F-001 (Distance), F-003 (Cost)
- ADR: adr-1.0.2-geo-calculation-methods.md
