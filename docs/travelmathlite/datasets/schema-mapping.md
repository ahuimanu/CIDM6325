# Schema Mapping: OurAirports CSV → Airport Model

## Overview

This document provides a comprehensive mapping between the OurAirports CSV dataset and the TravelMathLite `Airport` Django model, including field transformations, validation rules, and normalization logic.

**Date**: 2025-11-04  
**ADR**: adr-1.0.1-dataset-source-for-airports-and-cities.md  
**Brief**: ADR-1.0.1-04  
**Issue**: #33

---

## Field Mapping Table

| CSV Column       | Model Field      | Type    | Transform/Notes                                    | Required | Default |
|------------------|------------------|---------|----------------------------------------------------|----------|---------|
| `ident`          | `ident`          | string  | Direct mapping (ICAO or local code)                | Yes      | N/A     |
| `iata_code`      | `iata_code`      | string  | Direct mapping (3-letter code)                     | No       | `""`    |
| `name`           | `name`           | string  | Direct mapping                                     | Yes      | N/A     |
| `type`           | `airport_type`   | string  | Direct mapping (e.g., `large_airport`)             | Yes      | N/A     |
| `latitude_deg`   | `latitude_deg`   | float   | Validate: -90 ≤ value ≤ 90                         | Yes      | N/A     |
| `longitude_deg`  | `longitude_deg`  | float   | Validate: -180 ≤ value ≤ 180                       | Yes      | N/A     |
| `elevation_ft`   | `elevation_ft`   | int     | Parse to int; null if empty/invalid                | No       | `null`  |
| `iso_country`    | `iso_country`    | string  | Direct mapping (ISO 3166-1 alpha-2)                | Yes      | N/A     |
| `iso_region`     | `iso_region`     | string  | Direct mapping (ISO 3166-2)                        | No       | `""`    |
| `municipality`   | `municipality`   | string  | Direct mapping (city/town name)                    | No       | `""`    |
| N/A              | `created_at`     | datetime| Auto-generated on creation                         | Yes      | `now()` |
| N/A              | `updated_at`     | datetime| Auto-updated on save                               | Yes      | `now()` |

---

## Normalization Rules

### 1. Primary Key Strategy
- **CSV Source**: `ident` field (ICAO or local code)
- **Model**: `ident` CharField with `unique=True`
- **Rationale**: Ensures idempotent imports via `update_or_create()`

### 2. Coordinate Validation
- **Latitude**: Must be between -90.0 and 90.0 (inclusive)
- **Longitude**: Must be between -180.0 and 180.0 (inclusive)
- **Action on Invalid**: Log warning, skip row, increment error counter

### 3. Optional Field Handling
- **IATA Code**: Empty string if missing (not null for search optimization)
- **Elevation**: `null` if missing or unparseable
- **Region/Municipality**: Empty string if missing

### 4. Type Preservation
- **CSV Type Field**: Preserved as-is (e.g., `large_airport`, `medium_airport`, `small_airport`)
- **Future Enhancement**: Consider enum/choices for type validation

---

## Import Logic

### Upsert Strategy
```python
Airport.objects.update_or_create(
    ident=row["ident"],  # Lookup key
    defaults={
        "iata_code": row.get("iata_code", ""),
        "name": row["name"],
        "airport_type": row["type"],
        "latitude_deg": float(row["latitude_deg"]),
        "longitude_deg": float(row["longitude_deg"]),
        "elevation_ft": parse_elevation(row.get("elevation_ft")),
        "iso_country": row["iso_country"],
        "iso_region": row.get("iso_region", ""),
        "municipality": row.get("municipality", ""),
    }
)
```

### Filtering Logic (Import Command)
1. **IATA Filter** (`--filter-iata`): Skip rows without IATA code
2. **Limit** (`--limit N`): Stop after N rows (testing)
3. **Type Filter** (Future): Filter by airport type (e.g., exclude heliports)

### Error Handling
- **Missing Required Field**: Log warning, skip row, continue import
- **Invalid Coordinates**: Log warning, skip row, continue import
- **Duplicate Ident**: Update existing record (idempotent)
- **CSV Parse Error**: Report error, abort import

---

## Validation Rules

### Model-Level Validation
- **`ident`**: Unique constraint enforced by database
- **`iata_code`**: Indexed for fast lookup (not unique; some airports share codes)
- **Coordinates**: Django FloatField accepts valid floats; range validation in import command
- **Required Fields**: Django enforces `blank=False` on `name`, `airport_type`, `latitude_deg`, `longitude_deg`, `iso_country`

### Import Command Validation
```python
def _validate_row(row: dict[str, str]) -> None:
    # Check required fields present
    required = ["ident", "name", "latitude_deg", "longitude_deg", "iso_country"]
    for field in required:
        if not row.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    # Validate coordinate ranges
    lat = float(row["latitude_deg"])
    lon = float(row["longitude_deg"])
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}")
```

---

## Sample Data Mappings

### Example 1: Large Airport with IATA Code
**CSV Row:**
```csv
id,ident,type,name,latitude_deg,longitude_deg,elevation_ft,iso_country,iso_region,municipality,iata_code
3682,KDEN,large_airport,Denver International Airport,39.8561,-104.6737,5434,US,US-CO,Denver,DEN
```

**Model Instance:**
```python
Airport(
    ident="KDEN",
    iata_code="DEN",
    name="Denver International Airport",
    airport_type="large_airport",
    latitude_deg=39.8561,
    longitude_deg=-104.6737,
    elevation_ft=5434,
    iso_country="US",
    iso_region="US-CO",
    municipality="Denver",
)
```

### Example 2: Small Airport without IATA Code
**CSV Row:**
```csv
id,ident,type,name,latitude_deg,longitude_deg,elevation_ft,iso_country,iso_region,municipality,iata_code
323537,00AA,small_airport,Aero B Ranch Airport,38.704022,-101.473911,3435,US,US-KS,Leoti,
```

**Model Instance:**
```python
Airport(
    ident="00AA",
    iata_code="",  # Empty string, not null
    name="Aero B Ranch Airport",
    airport_type="small_airport",
    latitude_deg=38.704022,
    longitude_deg=-101.473911,
    elevation_ft=3435,
    iso_country="US",
    iso_region="US-KS",
    municipality="Leoti",
)
```

---

## Performance Considerations

### Database Indexes
```python
class Meta:
    indexes = [
        models.Index(fields=["iata_code"]),       # Fast IATA lookups
        models.Index(fields=["iso_country"]),     # Country filtering
        models.Index(fields=["latitude_deg", "longitude_deg"]),  # Spatial queries
    ]
```

### Import Performance
- **Dataset Size**: ~70,000 airports in full CSV (~30MB)
- **Import Time**: ~1 minute for full dataset on modern hardware
- **Memory Usage**: Streaming CSV parser (row-by-row, low memory)
- **Database**: Bulk upsert via `update_or_create()` (handles duplicates gracefully)

---

## Testing Coverage

### Validation Tests (`tests_validation.py`)
- Required fields enforced
- Latitude range: -90 to 90
- Longitude range: -180 to 180
- `ident` uniqueness constraint
- Optional fields (IATA, elevation, municipality) allow empty/null
- String representation with/without IATA code

### Import Tests (`tests_import.py`)
- Dry-run mode (no database writes)
- Create new airports
- Idempotent updates (re-import same data)
- Limit flag (`--limit`)
- Filter IATA flag (`--filter-iata`)
- Invalid coordinates handling
- Missing required fields handling

---

## Future Enhancements

### Phase 2 Considerations
1. **Airport Type Enum**: Convert `airport_type` to Django choices field
2. **Spatial Queries**: Add PostGIS support for advanced distance calculations
3. **Data Quality Scores**: Track completeness/accuracy per airport
4. **Incremental Updates**: Track last_updated from CSV, only import changed records
5. **City Normalization**: Link to separate City model (reduce duplication)

### Data Quality Improvements
1. **IATA Code Deduplication**: Handle cases where multiple airports share IATA codes
2. **Name Standardization**: Normalize airport names (e.g., "Intl" vs "International")
3. **Coordinate Precision**: Round coordinates to consistent decimal places
4. **Elevation Validation**: Cross-check elevation with third-party sources

---

## References

- **Dataset Documentation**: `docs/travelmathlite/datasets/ourairports.md`
- **Model Definition**: `travelmathlite/apps/airports/models.py`
- **Import Command**: `travelmathlite/apps/airports/management/commands/import_airports.py`
- **ADR**: `docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md`
- **OurAirports Schema**: https://ourairports.com/help/data-dictionary.html

---

## Change Log

| Date       | Version | Changes                                              | Author  |
|------------|---------|------------------------------------------------------|---------|
| 2025-11-04 | 1.0.0   | Initial schema mapping documentation for Brief-04    | System  |

