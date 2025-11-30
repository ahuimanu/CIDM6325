# ADR-1.0.1 Dataset source for airports and cities

Date: 2025-11-02  
Status: Accepted  
Version: 1.0  
Authors: Course Staff  
Reviewers: Completed (Brief ADR-1.0.1-01)  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#14-open-questions (Open questions)  
Scope IDs from PRD: F-002, F-004, F-005, F-008  
Functional requirements: FR-F-002-1, FR-F-004-1, FR-F-005-1, FR-F-008-1  
Related issues or PRs: #30

---

## Intent and scope

Choose a canonical open dataset for airports (and optionally cities) to support nearest-airport lookup, search, and admin import.

In scope: dataset selection, licensing, expected fields, import approach.  
Out of scope: detailed model schema (covered by ADR-1.0.3) and search UX specifics.

---

## Problem and forces

- Need consistent, reliable airport data including IATA/ICAO codes and coordinates.
- Forces: data quality, permissive license, stable URLs, predictable CSV formats, minimal preprocessing.
- Constraints: Internet access may be limited; import must be idempotent and support local files.

---

## Options considered

- A) OurAirports (CSV) <https://ourairports.com/data/>

  - Pros
    - Clear CSVs; permissive license; includes lat/long, IATA/ICAO, city/country
  - Cons
    - Some records missing IATA codes; requires filtering
  - Notes
    - Common in teaching; aligns with import command simplicity

- B) OpenFlights (airports.dat)

  - Pros
    - Popular; compact
  - Cons
    - Non-CSV quirks; licensing ambiguity; schema less clear
  - Notes
    - Additional parsing overhead for students

- C) GeoNames (cities)

  - Pros
    - Rich place data
  - Cons
    - Heavier; account needed for some endpoints; overkill for MVP
  - Notes
    - Could complement later

---

## Decision

We choose A (OurAirports) because it balances quality, license clarity, and CSV simplicity for an idempotent import command.

Decision drivers ranked: ease-of-import, license clarity, field coverage.

---

## Consequences

Positive

- CSV import via `import_airports` is straightforward
- Fields map cleanly to Airport model (name, iata_code, iso_country, latitude_deg, longitude_deg)

Negative and risks

- Missing IATA codes for some airports; city names vary

Mitigations

- Filter to airports with IATA where needed; provide admin tools to merge/flag

---

## Requirements binding

- FR-F-005-1 Implement `import_airports` idempotently with `--dry-run` (Trace F-005)
- FR-F-004-1 Airport model includes indexes and search fields (Trace F-004)
- FR-F-002-1 Nearest-airport uses lat/long from dataset (Trace F-002)
- NF-004 Reliability: validate row counts; log progress

---

## Acceptance criteria snapshot

- AC: `import_airports --dry-run` reports parsed rows and upserts without duplicates
- AC: Admin can search airports by IATA/city/country

Evidence to collect

- CLI transcript of import; admin screenshots

---

## Implementation outline

Plan

- Download OurAirports CSVs (airports.csv; optionally countries.csv) to `downloads/` or fetch via URL
- Parse with Python csv; validate required fields; upsert by `ident` or IATA
- Add indexes on `iata_code`, `(latitude, longitude)`

Denied paths

- No runtime dependency on external paid APIs

Artifacts to update

- `apps/airports/management/commands/import_airports.py`, models, admin

---

## Test plan and invariants

Invariants

- INV-1 Import is idempotent; running twice yields same row counts
- INV-2 Invalid rows are skipped with logged warnings

Unit tests

- Tests for command dry-run and commit; sample CSV fixture

Behavioral tests

- Admin search flow exercises imported records

---

## Schema mapping and normalization

Field mapping documentation

- Comprehensive schema mapping in `apps/airports/schema_mapping.py`
- Documentation in `docs/travelmathlite/schema-mapping-airports.md`
- 13 mapped fields from OurAirports CSV to Airport model (including normalized FK placeholders and active flag)
- 8 unmapped fields explicitly documented with rationale

Normalization function

- `normalize_csv_row()` converts CSV strings to model types
- Type conversions: coordinates (str→float), elevation (str→int/None)
- Field name mapping: CSV 'type' → model 'airport_type'
- Validation: coordinate ranges, required fields

Test coverage

- 17 schema mapping tests in `tests_schema_mapping.py`
- Tests for complete/minimal rows, conversions, validation, edge cases
- Integration tests verify model compatibility

---

## Integration with core models

- **Normalized models**: Created `Country`/`City` in `apps/base/models.py` with admin coverage and migrations (`base/0001_initial.py`), extending Airport via `airports/0002_airport_core_integrations.py`.
- **Linking service**: `apps/airports/services/integration.py` links dataset rows to normalized models, caches lookups, and powers the enhanced importer stats plus new guard flags (`--skip-country-link`, `--skip-city-link`).
- **Command + validation updates**: `import_airports` now reports linkage coverage and `validate_airports` surfaces normalized FK health; QuerySet helpers expose `nearest()` distance calculations with bounding-box pre-filters.
- **Documentation & tests**: Added `docs/travelmathlite/data-model-integration.md` runbook, expanded `schema-mapping-airports.md` with FK heuristics, and added Django tests covering importer linking + manager behavior (`apps/base/tests/test_models.py`, `apps/airports/tests_city_country_integration.py`).

---

## Documentation updates

- Add docs/datasets/ourairports.md with fields used and filters applied
- README quickstart for running the import
- Schema mapping documentation: docs/travelmathlite/schema-mapping-airports.md

---

## Rollback and contingency

Rollback trigger

- Import performance or data quality unacceptable

Rollback steps

- Switch to OpenFlights parser module (kept behind feature flag)

Data and config safety

- No destructive migrations; transactional bulk upserts

---

## Update automation and sync strategy

Update automation command

- `update_airports` management command provides scheduled update capability
- Wraps `import_airports` with timing, logging, error handling, and reporting
- Supports `--dry-run` for testing update logic without database changes
- Transaction-safe: rollback on failure, commit only on success

Scheduling strategies

- **Cron**: Daily/weekly scheduled updates via system cron or django-crontab
- **Celery Beat**: For applications with existing Celery infrastructure
- **Manual**: On-demand updates during development or maintenance windows

Update frequency recommendations

- Production: Weekly updates (OurAirports changes infrequently)
- IATA-only: Daily updates (more stable subset)
- Development: On-demand as needed

Error handling and monitoring

- Network failures caught and logged; database unchanged on error
- Validation errors skip invalid rows; valid data still imported
- Summary reporting: initial/final counts, net change, duration, error counts
- Logging to Python logging system for centralized monitoring
- Alert on: failed updates, excessive duration, high error rate, data staleness

Idempotent updates

- Uses `update_or_create()` for upsert operations
- Existing airports updated with latest data
- New airports created in database
- Removed airports preserved (no deletions)

Performance considerations

- Processes 70K airports in ~2-3 minutes
- Row-by-row processing with minimal memory footprint
- Single transaction for consistency
- Filter by `--filter-iata` for focused updates on relevant airports

Backup and rollback

- Pre-update backups recommended for production
- Dry-run testing before production updates
- Database restore procedure documented for emergency rollback

Security and compliance

- HTTPS by default for data source downloads
- OurAirports data is public domain (attribution appreciated)
- No API keys or credentials required
- Data validation prevents malformed data

Test coverage

- Update command tests in `tests_update_command.py` (10 tests)
- Coverage includes: dry-run mode, filtering, error handling, timing, integration

Documentation

- Comprehensive update automation guide: `docs/travelmathlite/update-automation-airports.md`
- Includes: cron examples, monitoring strategies, troubleshooting, performance tips

---

## Validation and data quality

Validation command

- `validate_airports` management command provides data quality reporting
- Validates required fields, coordinate ranges, uniqueness, and format rules
- Reports anomalies with optional verbose mode for detailed diagnostics
- Checks: latitude (-90 to 90), longitude (-180 to 180), IATA code format (3 letters), ISO country code format (2 letters)

Test coverage

- Model validation tests in `tests_validation.py` (9 tests)
- Command validation tests in `tests_validate_command.py` (9 tests)
- Coverage includes edge cases, anomaly detection, and reporting

---

## Licensing and compliance

OurAirports license

- **License**: Public Domain
- **Terms**: All data released to Public Domain with no restrictions
- **Source**: <https://ourairports.com/data/>
- **Official Statement**: "All data is released to the Public Domain, and comes with no guarantee of accuracy or fitness for use."

Permitted uses

- ✅ Commercial use without restriction
- ✅ Modification and derivative works
- ✅ Redistribution in any format
- ✅ No attribution required (but appreciated)
- ✅ No API keys or registration needed

Warranty disclaimer

- ❌ No warranty of accuracy
- ❌ No warranty of fitness for purpose
- ❌ No liability for errors or omissions
- ✅ TravelMathLite implements validation and error handling to mitigate risks

Attribution practice

- **Provided**: Optional attribution included in documentation as best practice
- **Text**: "Airport data sourced from OurAirports (<https://ourairports.com/data/>), released to the Public Domain."
- **Locations**: ADR documentation, README, code comments
- **Rationale**: Respects open data norms, builds trust, aids transparency

Risk assessment

- **License Risk**: Very Low (Public Domain is irrevocable for released data)
- **Data Quality Risk**: Low (validation checks, dry-run testing, error handling)
- **Operational Risk**: Very Low (error handling, local caching, no rate limits)
- **Overall Status**: ✅ Compliant with low risk profile

Compliance obligations

- **Legal Requirements**: None (Public Domain dedication removes all obligations)
- **Best Practices**: Attribution provided, accuracy disclaimers noted, license documented
- **Monitoring**: Annual review of license status (no changes expected)
- **Documentation**: Comprehensive compliance review in `docs/travelmathlite/licensing-compliance-airports.md`

Alternative sources considered

- **OpenFlights**: ODbL license (attribution + share-alike) - more restrictive
- **Commercial APIs**: Proprietary terms, costs, rate limits - higher complexity
- **Government sources**: Variable licensing, less comprehensive coverage

Compliance checklist

- [x] Verify Public Domain status of OurAirports data
- [x] Document license terms in ADR
- [x] Create comprehensive compliance documentation
- [x] Provide attribution in documentation
- [x] Implement data validation (validate_airports)
- [x] Add error handling for data quality issues
- [x] Test with dry-run mode
- [x] Review and accept "no warranty" implications
- [ ] Consider user-facing attribution (About page, API metadata)
- [ ] Add disclaimers to Terms of Service (if created)

---

## Attestation plan

Human witness

- Student demonstrates `--dry-run` and import in class or via transcript

Attestation record

- Commit hash for command; screenshot paths in docs

---

## Checklist seed

- [x] CSV import dry-run and commit paths implemented
- [x] Indexes created and migration added
- [x] Admin search tested
- [x] Data validation command implemented
- [x] Validation tests with 100% coverage

---

## References

- PRD §4 F-002/F-004/F-005, §14 Open questions
