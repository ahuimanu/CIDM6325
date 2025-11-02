# ADR-1.0.0 Application architecture and app boundaries

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#13-traceability (Traceability)  
Scope IDs from PRD: F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015  
Functional requirements: FR-F-001-1, FR-F-001-2, FR-F-002-1, FR-F-003-1, FR-F-004-1, FR-F-005-1, FR-F-006-1, FR-F-007-1, FR-F-008-1, FR-F-009-1, FR-F-010-1, FR-F-011-1, FR-F-012-1, FR-F-013-1, FR-F-014-1, FR-F-015-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define the Django project module boundaries using multiple small apps under `apps/*` to match domain concerns (calculators, airports, accounts, trips, search, core) and keep templates and URLs namespaced.  
In scope: app layout, import paths, template directories, namespaced URLs, shared `core/` helpers.  
Out of scope: specific model fields, specific calculations (covered by separate ADRs).

---

## Problem and forces

- Need clear separation of concerns for teaching, maintainability, and testing.
- Forces: simplicity for students vs. realism of production app layout; reuse across calculators; URL reversibility and namespacing.
- Constraints: Use Django, Bootstrap 5, HTMX; small repo with understandable structure.

---

## Options considered

- A) Single monolithic `app` containing everything
  - Pros: simplest wiring, fewer imports
  - Cons: low cohesion, hard to test, noisy admin and URLs
  - Notes: Strains F-004 admin, F-011 tests
- B) Multiple apps by domain (`apps/calculators`, `apps/airports`, `apps/accounts`, `apps/trips`, `apps/search`, `apps/core`)
  - Pros: clear boundaries, better tests, reuse, namespacing
  - Cons: a bit more boilerplate
  - Notes: Aligns to PRD Sections 4 and 13
- C) Micro-app per feature (very granular)
  - Pros: maximal isolation
  - Cons: overhead too high for course pace
  - Notes: Overkill

---

## Decision

We choose B because it balances clarity and simplicity while matching PRD domain slices.  
Decision drivers ranked: cohesion, testability, student comprehension.

---

## Consequences

Positive

- Easier to locate code; clearer ownership per feature
- Tests can target app modules

Negative and risks

- Slightly more files and wiring

Mitigations

- Provide a project layout guide in docs; consistent app scaffolds

---

## Requirements binding

- FR-F-004-1 Models and admin live in domain apps with indexes and managers (Trace F-004)
- FR-F-007-1 Templates organized under app namespaces (Trace F-007)
- FR-F-008-1 Namespaced URLs for search and calculators (Trace F-008)
- NF-004 Health check wired at project level; core middleware centralized

---

## Acceptance criteria snapshot

- AC: `apps/*` directory exists with calculators, airports, accounts, trips, search, core
- AC: Each app has `urls.py` and templates under `templates/<app>/...`
- AC: Project `urls.py` includes namespaced app URLs

Evidence to collect

- Tree listing; sample reverse() usages; screenshots of pages

---

## Implementation outline

Plan

- Create `apps/*` with minimal `apps.py`, `urls.py`, `views.py`, `templates/`
- Configure `INSTALLED_APPS` in settings
- Project `urls.py` includes app URLConfs under namespaces

Denied paths

- No single-app monolith

Artifacts to update

- Settings, project `urls.py`, per-app templates

---

## Test plan and invariants

Invariants

- INV-1 All URLs reverse via namespaces
- INV-2 Templates per app resolve without conflicts

Unit tests

- `apps/*/tests.py` for URL reversing and template rendering

Behavioral tests

- Navigation through navbar across apps

---

## Documentation updates

- Add docs/architecture/app-layout.md
- Update README with app structure

---

## Rollback and contingency

Rollback trigger

- Confusion in imports, collisions in templates

Rollback steps

- Consolidate fewer apps (calculators + airports), then re-split later

Data and config safety

- Pure wiring; no data migration impact

---

## Attestation plan

Human witness

- Instructor review of layout

Attestation record

- Commit hashes introducing app scaffolds

---

## Checklist seed

- [ ] Namespaced URLs included
- [ ] INSTALLED_APPS configured
- [ ] Templates organized by app

---

## References

- PRD §4 Scope, §13 Traceability
