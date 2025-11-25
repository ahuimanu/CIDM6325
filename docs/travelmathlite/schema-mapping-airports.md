# Airport Schema Mapping Documentation

This document describes how the OurAirports dataset is mapped to the TravelMathLite Airport model.

## Overview

The Airport model is designed to store airport data from the [OurAirports](https://ourairports.com/data/) dataset, which provides comprehensive, public domain airport information.

## Dataset Source

- **Source**: OurAirports (https://davidmegginson.github.io/ourairports-data/airports.csv)
- **License**: Public Domain
- **Format**: CSV with header row
- **Update Frequency**: Updated regularly by community contributors

## Field Mapping

### Mapped Fields

The following fields from the OurAirports CSV are mapped to our Airport model:

| Model Field | CSV Field | Type | Required | Description | Example |
|------------|-----------|------|----------|-------------|---------|
| `ident` | `ident` | str | Yes | ICAO or local airport code (unique identifier) | KDEN |
| `iata_code` | `iata_code` | str | No | IATA 3-letter code (preferred for display) | DEN |
| `name` | `name` | str | Yes | Airport name | Denver International Airport |
| `airport_type` | `type` | str | No | Airport type category | large_airport |
| `latitude_deg` | `latitude_deg` | float | Yes | Latitude in decimal degrees (-90 to 90) | 39.8561 |
| `longitude_deg` | `longitude_deg` | float | Yes | Longitude in decimal degrees (-180 to 180) | -104.6737 |
| `elevation_ft` | `elevation_ft` | int | No | Elevation in feet | 5434 |
| `iso_country` | `iso_country` | str | Yes | ISO 3166-1 alpha-2 country code | US |
| `iso_region` | `iso_region` | str | No | ISO 3166-2 region code | US-CO |
| `municipality` | `municipality` | str | No | City or town name | Denver |
| `country` | Derived from `iso_country` | FK (apps.base.Country) | No | Normalized Country row linked via integrator | Country(id=US) |
| `city` | Derived from (`municipality`, `iso_country`) | FK (apps.base.City) | No | Normalized City row linked via integrator | City(name=Denver) |
| `active` | Derived from `type` | bool | No | Indicates whether airport is operational (`type != "closed"`) | True |

### Unmapped Fields

The following OurAirports CSV fields are intentionally **not** mapped to our model:

- `id` - OurAirports internal ID (not needed; we use `ident` as primary key)
- `continent` - Can be derived from `iso_country` if needed
- `scheduled_service` - Not relevant for MVP functionality
- `gps_code` - Redundant with `ident`/`iata_code`
- `local_code` - Redundant with `ident`
- `home_link` - Airport website URLs (not in scope)
- `wikipedia_link` - Wikipedia URLs (not in scope)
- `keywords` - Search keywords (not needed for core functionality)

## Data Transformations

### Type Conversions

1. **Coordinates** (latitude_deg, longitude_deg)
   - Input: String in CSV
   - Output: Float in model
   - Validation: Range checks (-90 to 90 for lat, -180 to 180 for lon)

2. **Elevation** (elevation_ft)
   - Input: String in CSV (may be empty or decimal)
   - Output: Integer in model or NULL
   - Handling: Converts decimal to int; invalid values become NULL

3. **Field Name Mapping**
   - CSV `type` → Model `airport_type` (avoids Python reserved word)

### Normalization Rules

1. **Empty Strings**: Optional string fields with empty values are stored as empty strings (not NULL)
2. **Missing Optional Fields**: If a field is not present in CSV, it defaults to empty string or NULL (for elevation)
3. **Whitespace**: No special trimming; values are stored as provided in CSV
4. **Case Sensitivity**: Values are case-sensitive and stored as-is

### Normalized Country/City linkage

- `apps/airports/services/integration.py` reads `iso_country` + `municipality` to create/link `apps.base.Country` and `apps.base.City` records (with lightweight caching and optional `downloads/countries.csv` lookup).
- Import stats now surface linkage coverage along with creation counts; guard flags `--skip-country-link` / `--skip-city-link` keep debugging flexible.
- When municipalities are blank we skip city linking; coverage ratios are reported via `manage.py validate_airports` to highlight orphaned rows.

## Airport Types

Common values found in the `airport_type` field:

- `large_airport` - Major commercial airports
- `medium_airport` - Regional airports
- `small_airport` - Local and private airports
- `heliport` - Helicopter landing sites
- `seaplane_base` - Water landing facilities
- `balloonport` - Balloon launch sites
- `closed` - Permanently closed airports

## Example Mapping

### Input (CSV Row)
```csv
id,ident,type,name,latitude_deg,longitude_deg,elevation_ft,continent,iso_country,iso_region,municipality,scheduled_service,gps_code,iata_code,local_code,home_link,wikipedia_link,keywords
3462,KDEN,large_airport,Denver International Airport,39.861698150635,-104.672996521,5434,NA,US,US-CO,Denver,yes,KDEN,DEN,DEN,http://www.flydenver.com/,https://en.wikipedia.org/wiki/Denver_International_Airport,Denver
```

### Output (Model Fields)
```python
{
    "ident": "KDEN",
    "iata_code": "DEN",
    "name": "Denver International Airport",
    "airport_type": "large_airport",
    "latitude_deg": 39.861698150635,
    "longitude_deg": -104.672996521,
    "elevation_ft": 5434,
    "iso_country": "US",
    "iso_region": "US-CO",
    "municipality": "Denver",
    "country": "United States (US)",
    "city": "Denver, US",
    "active": True,
}
```

## Validation Rules

The import process validates data according to these rules:

1. **Required Fields**: Must be present and non-empty
   - `ident`, `name`, `latitude_deg`, `longitude_deg`, `iso_country`

2. **Coordinate Ranges**:
   - Latitude: -90.0 ≤ value ≤ 90.0
   - Longitude: -180.0 ≤ value ≤ 180.0

3. **IATA Code Format** (when present):
   - Exactly 3 uppercase letters
   - Empty string if not available

4. **ISO Country Code**:
   - Exactly 2 uppercase letters (ISO 3166-1 alpha-2)

5. **Uniqueness**:
   - `ident` must be unique across all airports
   - Database constraint enforces this

## Usage

### Import Command

```bash
# Import from URL (default)
python manage.py import_airports

# Import from local file
python manage.py import_airports --file downloads/airports.csv

# Dry run to validate without saving
python manage.py import_airports --dry-run

# Filter to only airports with IATA codes
python manage.py import_airports --filter-iata

# Limit import for testing
python manage.py import_airports --limit 100

# Skip normalized linkage (debugging only)
python manage.py import_airports --skip-country-link --skip-city-link
```

### Programmatic Usage

```python
from apps.airports.schema_mapping import normalize_csv_row

# Read CSV row
csv_row = {
    "ident": "KDEN",
    "type": "large_airport",
    "name": "Denver International Airport",
    "latitude_deg": "39.8561",
    "longitude_deg": "-104.6737",
    # ... other fields
}

# Normalize to model fields
normalized = normalize_csv_row(csv_row)

# Create or update airport
from apps.airports.models import Airport
airport, created = Airport.objects.update_or_create(
    ident=normalized["ident"],
    defaults=normalized
)

# Link normalized Country/City (normally handled by import_airports)
from apps.airports.services import AirportLocationIntegrator

integrator = AirportLocationIntegrator()
location = integrator.link_location(
    iso_country=normalized["iso_country"],
    municipality=normalized["municipality"],
    latitude=normalized["latitude_deg"],
    longitude=normalized["longitude_deg"],
)
airport.country = location.country
airport.city = location.city
airport.save()
```

## Testing

Schema mapping tests are in `tests_schema_mapping.py`:

```bash
# Run schema mapping tests
python manage.py test apps.airports.tests_schema_mapping

# Run all airport tests
python manage.py test apps.airports
```

## References

- ADR-1.0.1: Dataset source for airports and cities
- OurAirports Data: https://ourairports.com/data/
- ISO 3166 Country Codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
- IATA Airport Codes: https://en.wikipedia.org/wiki/IATA_airport_code
- Data model integration runbook: `docs/travelmathlite/data-model-integration.md`
