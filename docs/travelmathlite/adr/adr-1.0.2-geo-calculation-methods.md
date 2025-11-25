# ADR-1.0.2 Geo calculation methods (distance, time, cost)

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-001, F-003  
Functional requirements: FR-F-001-1, FR-F-001-2, FR-F-003-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define how we compute straight-line (flight) distance, approximate driving distance/time, and cost-of-driving.

In scope: algorithms, libraries, units, configurable defaults.  
Out of scope: real-time routing or traffic APIs.

---

## Problem and forces

- Need reproducible distance/time outputs without paid APIs.
- Forces: pedagogical simplicity, reasonable accuracy, testability, unit handling.
- Constraints: No external routing API; rely on haversine/geodesic formulas and heuristics.

---

## Options considered

- A) Geodesic/haversine via a small library (e.g., geopy or our own function)

  - Pros
    - Deterministic, no network, easy to test
  - Cons
    - Flight distance only; driving distance is heuristic
  - Notes
    - Adequate for PRD purposes

- B) External routing services (e.g., OSRM/Mapbox/Google)

  - Pros
    - Real driving routes and times
  - Cons
    - Keys, quotas, cost, network; complexity for course
  - Notes
    - Overkill for MVP

---

## Decision

We choose A (geodesic/haversine) for flight distance and a configurable heuristic for driving distance/time: driving_distance ≈ straight_line_km × route_factor (default 1.2), driving_time ≈ driving_distance / avg_speed_kmh (default 80 km/h). Cost-of-driving uses distance, fuel economy, and fuel price.

Decision drivers ranked: offline, simple, configurable.

---

## Consequences

Positive

- No network dependencies; deterministic tests
- Clear knobs via settings for route_factor and avg_speed

Negative and risks

- Results are approximate and may differ from real-world routes

Mitigations

- Document assumptions; allow user overrides via form fields; keep defaults in settings

---

## Requirements binding

- FR-F-001-1 Compute flight and driving outputs with unit selection (Trace F-001)
- FR-F-001-2 Validate inputs (city/airport/lat-long) and normalize to coordinates (Trace F-001)
- FR-F-003-1 Compute cost-of-driving with defaults and overrides (Trace F-003)
- NF-001 Performance: p95 < 700 ms for compute-heavy endpoints

---

## Acceptance criteria snapshot

- AC: Given two coordinates, function returns geodesic distance and heuristic driving time
- AC: Cost calculator returns value from inputs or defaults; units displayed correctly

Evidence to collect

- Unit test outputs for known city pairs; screenshots of calculator page

---

## Implementation outline

Plan

- Add `calculators/geo.py` with haversine/geodesic and helpers for unit conversion
- Add settings for `ROUTE_FACTOR` and `AVG_SPEED_KMH`; expose as defaults in forms
- Implement `calculators/costs.py` to compute cost; wire to forms and HTMX partials

Denied paths

- No integration with external routing APIs in MVP

Artifacts to update

- `apps/calculators/` modules, settings, forms, templates

---

## Test plan and invariants

Invariants

- INV-1 Conversions between miles ↔ km are correct
- INV-2 Cost computation is deterministic for given inputs

Unit tests

- Tests for `geo.py` and `costs.py` with fixed city coordinates; freeze time if needed

Behavioral tests

- Form validation and HTMX partial updates

---

## Documentation updates

- docs/algorithms/distance-and-cost.md covering formulas and defaults
- README quickstart with example inputs/outputs

---

## Rollback and contingency

Rollback trigger

- Accuracy complaints; performance regressions

Rollback steps

- Adjust defaults; add alternate formula behind a flag

Data and config safety

- Pure compute; no data migrations

---

## Attestation plan

Human witness

- Reviewer validates unit tests and cross-checks one city pair manually

Attestation record

- Commit hashes for `geo.py` and tests; doc link

---

## Checklist seed

- [ ] Haversine/geodesic implemented with tests
- [ ] Heuristic driving time and cost functions implemented
- [ ] Settings defaults wired; form overrides work

---

## References

- PRD §4 F-001/F-003; §7 NF-001 performance
