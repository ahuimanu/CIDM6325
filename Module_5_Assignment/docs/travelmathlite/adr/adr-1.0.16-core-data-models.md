# ADR-1.0.16 Core data models (City, Airport, Country)

Date: 2025-11-02  
Status: Accepted (Brief ADR-1.0.1-07, Issue #39)  
Version: 1.0  
Authors: Course Staff  
Reviewers: Completed via Brief ADR-1.0.1-07

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope)  
Scope IDs from PRD: F-004, F-002  
Functional requirements: FR-F-004-1, FR-F-002-1  
Related issues or PRs: #39

---

## Intent and scope

Define normalized models for City, Airport, and Country with indexes and managers to support search and nearest-airport features.

In scope: fields, indexes, admin config, managers.  
Out of scope: user/trip models (covered elsewhere).

---

## Problem and forces

- Need maintainable schema that maps to dataset fields and supports fast lookups.
- Forces: import simplicity, admin usability, search performance.
- Constraints: SQLite-first; optional Postgres later.

---

## Options considered

- A) Separate City, Airport, Country models; Airport FK to City and Country (nullable where data missing)

  - Pros
    - Normalization; admin browsing; flexible search
  - Cons
    - More joins; data hygiene needed
  - Notes
    - Balanced approach

- B) Single Airport model with denormalized city/country strings

  - Pros
    - Simplest import
  - Cons
    - Harder filtering; repeated data
  - Notes
    - Not preferred

---

## Decision

We choose A. Models:

- Country: code (ISO), name
- City: name, country(FK), lat, lon, searchable_name
- Airport: ident, iata_code, icao_code, name, city(FK, null), country(FK), lat, lon, active flag

Indexes on codes and `(lat, lon)`; manager methods for case-insensitive search.

Decision drivers ranked: admin usability, search performance, import mapping.

---

## Consequences

Positive

- Clean admin with search and filters; flexible queries

Negative and risks

- Incomplete dataset linkage (missing city FK)

Mitigations

- Allow nulls and provide admin actions to fix/merge

---

## Requirements binding

- FR-F-004-1 Models with indexes and admin configs (Trace F-004)
- FR-F-002-1 Nearest-airport uses Airport lat/lon (Trace F-002)

---

## Acceptance criteria snapshot

- AC: Admin list/search works for Airport by code/name; filters by country
- AC: Queries for nearest airport use indexes to pre-filter

Evidence to collect

- Admin screenshots; explain query plan snippet

---

## Implementation outline

Plan

- Create models and migrations; add managers and admin classes
- Add index and unique constraints as needed
- Update import command to populate FKs when possible

Denied paths

- No denormalized-only schema

Artifacts to update

- `apps/airports/models.py`, `apps/core/models.py`, admin, migrations
  - Delivered as `apps/base/models.py`, `apps/base/admin.py`, `apps/airports/models.py`, with migrations `base/0001_initial.py`, `airports/0002_airport_core_integrations.py`

---

## Test plan and invariants

Invariants

- INV-1 Code uniqueness where appropriate (IATA/ICAO/ident)
- INV-2 Case-insensitive search finds expected records

Unit tests

- Model/manager tests; admin registration sanity

Behavioral tests

- Admin flows and nearest-airport end-to-end

---

## Documentation updates

- docs/data-models/airports.md
- `docs/travelmathlite/data-model-integration.md` (new runbook)

---

## Rollback and contingency

Rollback trigger

- Migration issues or poor performance

Rollback steps

- Adjust indexes; simplify FKs

Data and config safety

- Migrations reversible; keep backups in demo

---

## Attestation plan

Human witness

- Reviewer verifies admin and search performance

Attestation record

- Commit hash and screenshots

---

## Implementation results (2025-11-15)

- Models & migrations landed for `Country`/`City` plus Airport FK + `active` flag; admin dashboards expose filters/search + read-only timestamps.
- Importer updated with `AirportLocationIntegrator`, typed QuerySet helpers (`active()`, `search()`, `nearest()`), and validation now reports normalized linkage coverage.
- Tests cover Country/City normalization, importer FK creation, QuerySet behavior, and command regression; docs updated with integration playbook.

## Checklist seed

- [x] Models and migrations created
- [x] Admin search/filters configured
- [x] Indexes present on codes and lat/lon

---

## References

- PRD §4 F-004; §14 Open questions
