# ADR-1.0.1 Dataset source for airports and cities

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#14-open-questions (Open questions)  
Scope IDs from PRD: F-002, F-004, F-005, F-008  
Functional requirements: FR-F-002-1, FR-F-004-1, FR-F-005-1, FR-F-008-1  
Related issues or PRs: #TODO

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

## Documentation updates

- Add docs/datasets/ourairports.md with fields used and filters applied
- README quickstart for running the import

---

## Rollback and contingency

Rollback trigger

- Import performance or data quality unacceptable

Rollback steps

- Switch to OpenFlights parser module (kept behind feature flag)

Data and config safety

- No destructive migrations; transactional bulk upserts

---

## Attestation plan

Human witness

- Student demonstrates `--dry-run` and import in class or via transcript

Attestation record

- Commit hash for command; screenshot paths in docs

---

## Checklist seed

- [ ] CSV import dry-run and commit paths implemented
- [ ] Indexes created and migration added
- [ ] Admin search tested

---

## References

- PRD §4 F-002/F-004/F-005, §14 Open questions
