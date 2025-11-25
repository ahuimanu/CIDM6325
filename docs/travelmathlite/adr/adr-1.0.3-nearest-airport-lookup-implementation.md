# ADR-1.0.3 Nearest airport lookup implementation

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-002, F-004, F-005, F-013  
Functional requirements: FR-F-002-1, FR-F-004-1  
Related issues or PRs: #TODO

---

## Intent and scope

Choose how to compute the nearest airport(s) for a given city or coordinate using imported airport data.

In scope: query strategy, indexes, pagination/sorting.  
Out of scope: dataset selection (ADR-1.0.1), UI here (search ADR covers UX).

---

## Problem and forces

- Need fast nearest-neighbor lookup without PostGIS.
- Forces: SQLite-first development, optional Postgres in production, correctness, simplicity.
- Constraints: No geospatial extension; must work in-class environments.

---

## Options considered

- A) Python-side filtering using a coarse bounding box + precise haversine on candidates

  - Pros
    - Works on SQLite; straightforward
  - Cons
    - Some CPU work in Python; needs indexes to narrow candidates
  - Notes
    - Tunable bounding-box radius

- B) SQL annotation with haversine formula and ORDER BY computed distance

  - Pros
    - One query returns ordered results
  - Cons
    - Vendor-specific SQL; perf may be worse on SQLite without indexes
  - Notes
    - Harder to teach cross-DB

---

## Decision

We choose A (bounding box + Python haversine) with DB indexes on `(latitude, longitude)` and filters by country when applicable. Return top 3 results ordered by computed distance.

Decision drivers ranked: portability, simplicity, predictable performance.

---

## Consequences

Positive

- Works identically on SQLite and Postgres
- Easy to unit test; minimal SQL complexity

Negative and risks

- Potentially more Python work on large datasets

Mitigations

- Add indexes and sensible pre-filters; allow optional Postgres-specific path later

---

## Requirements binding

- FR-F-002-1 Top 3 nearest airports with distances (Trace F-002)
- FR-F-004-1 Indexes on lookups and managers for case-insensitive search (Trace F-004)
- NF-001 Performance: p95 lookup under 300 ms on sample dataset

---

## Acceptance criteria snapshot

- AC: For a known coordinate, nearest airports match expected order within reasonable tolerance
- AC: Query uses bounding box to limit candidate count

Evidence to collect

- Unit test on small fixture; log timing in local tests

---

## Implementation outline

Plan

- Add composite index or separate indexes on latitude/longitude
- Implement bbox filter: |lat - query_lat| <= dlat, |lon - query_lon| <= dlon
- Compute precise distances for candidates; sort in Python; return top 3

Denied paths

- No PostGIS or vendor-specific functions in MVP

Artifacts to update

- Airports manager/queryset, views, tests

---

## Test plan and invariants

Invariants

- INV-1 Ordering by computed distance is stable
- INV-2 Results include distances in consistent units

Unit tests

- Fixtures with 5–10 airports around a coordinate and expected ordering

Behavioral tests

- UI list shows top 3 sorted by distance with links

---

## Documentation updates

- docs/algorithms/nearest-airport.md

---

## Rollback and contingency

Rollback trigger

- Performance issues on full dataset

Rollback steps

- Switch to SQL annotation approach behind a setting flag

Data and config safety

- Index-only migrations; safe to revert

---

## Attestation plan

Human witness

- Reviewer validates test ordering and timing logs

Attestation record

- Commit hashes and test output snippet

---

## Checklist seed

- [ ] Indexes created
- [ ] BBox + Python sort implemented
- [ ] Tests added for expected order

---

## References

- PRD §4 F-002/F-004, §7 NF-001
