# OurAirports Dataset Documentation

## Overview

This document describes the OurAirports dataset selected for the TravelMathLite project, including field mappings, licensing, and rationale.

**Dataset Source**: [OurAirports](https://ourairports.com/data/)  
**License**: Public Domain (CC0)  
**Format**: CSV  
**Last Updated**: Regularly maintained by community

---

## Decision Summary

**Selected Dataset**: OurAirports (Option A)

**Alternatives Considered**:
- **OpenFlights**: Popular but has licensing ambiguity and non-CSV quirks
- **GeoNames**: Rich data but heavier, requires account for some endpoints, overkill for MVP

**Decision Drivers** (ranked):
1. Ease of import (CSV format)
2. License clarity (CC0/Public Domain)
3. Field coverage (IATA/ICAO, lat/long, city/country)

---

## Dataset Details

### Primary File: airports.csv

**URL**: https://davidmegginson.github.io/ourairports-data/airports.csv

**Key Fields Used**:

| Field Name       | Type   | Description                          | Required | Notes                           |
|------------------|--------|--------------------------------------|----------|---------------------------------|
| `id`             | int    | Internal OurAirports ID              | Yes      | Primary identifier              |
| `ident`          | string | ICAO or local code                   | Yes      | Fallback if IATA missing        |
| `type`           | string | Airport type (large/medium/small)    | Yes      | Filter for relevant types       |
| `name`           | string | Airport name                         | Yes      | Display name                    |
| `latitude_deg`   | float  | Latitude in decimal degrees          | Yes      | For distance calculations       |
| `longitude_deg`  | float  | Longitude in decimal degrees         | Yes      | For distance calculations       |
| `iata_code`      | string | IATA 3-letter code                   | No       | Preferred for search/display    |
| `iso_country`    | string | ISO 3166-1 country code              | Yes      | For filtering/grouping          |
| `iso_region`     | string | ISO 3166-2 region code               | No       | Additional context              |
| `municipality`   | string | City/town name                       | No       | Display and search              |

### Optional File: countries.csv

**URL**: https://davidmegginson.github.io/ourairports-data/countries.csv

Used for mapping `iso_country` codes to full country names for display purposes.

---

## Data Quality Notes

### Pros
- Clear CSV format with consistent schema
- Permissive CC0 license (Public Domain)
- Includes essential fields: IATA/ICAO, coordinates, city, country
- Regular community updates
- Stable URLs for automated downloads
- No authentication required

### Cons and Mitigations
- **Issue**: Some airports missing IATA codes
  - **Mitigation**: Filter to airports with IATA codes where needed; provide admin tools to flag/merge
- **Issue**: City names may vary in quality
  - **Mitigation**: Allow admin override; use `municipality` field as-is initially

---

## Import Strategy

### Filtering Rules
- Include airport types: `large_airport`, `medium_airport`, `small_airport`
- Exclude: `heliport`, `seaplane_base`, `balloonport`, `closed`
- Prefer records with IATA codes for primary features
- Validate required fields: `name`, `latitude_deg`, `longitude_deg`, `iso_country`

### Upsert Logic
- Primary key: `ident` (ICAO or local code)
- Secondary key: `iata_code` (when available)
- Update strategy: Replace existing records on re-import (idempotent)

### Performance Considerations
- CSV file size: ~30MB uncompressed
- Expected record count: ~70,000 total airports; ~10,000 with IATA codes
- Import time: <1 minute on modern hardware

---

## Licensing and Compliance

**License**: Public Domain (CC0 1.0 Universal)

**Obligations**: None (Public Domain dedication)

**Attribution**: Optional but recommended
- Suggested attribution: "Airport data from OurAirports (https://ourairports.com/)"

**Commercial Use**: Permitted without restrictions

**Redistribution**: Permitted without restrictions

**Legal Risks**: Minimal (Public Domain)

---

## References

- OurAirports Homepage: https://ourairports.com/
- Data Download Page: https://ourairports.com/data/
- License: https://creativecommons.org/publicdomain/zero/1.0/
- ADR: docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md
- PRD: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md §4 (F-002, F-004, F-005, F-008)

---

## Next Steps

1. Implement data ingestion pipeline (Brief ADR-1.0.1-02)
2. Create Airport model with indexes (ADR-1.0.16)
3. Build `import_airports` management command (Brief ADR-1.0.1-02)
4. Add data validation and quality checks (Brief ADR-1.0.1-03)
