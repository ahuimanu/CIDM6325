# ADR-1.0.0 Application architecture and app boundaries

Date: 2025-11-02  
Status: Accepted  
Version: 1.0  
Authors: Course Staff  
Reviewers: Completed via Briefs 01–06  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#13-traceability (Traceability)  
Scope IDs from PRD: F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015  
Functional requirements: FR-F-001-1, FR-F-001-2, FR-F-002-1, FR-F-003-1, FR-F-004-1, FR-F-005-1, FR-F-006-1, FR-F-007-1, FR-F-008-1, FR-F-009-1, FR-F-010-1, FR-F-011-1, FR-F-012-1, FR-F-013-1, FR-F-014-1, FR-F-015-1  
Related issues or PRs: #20 (Brief 01), #21 (Brief 02), #22 (Brief 03), #23 (Brief 04), #24 (Brief 05), #26 (Brief 06)

---

## Intent and scope

Define the Django project module boundaries using multiple small apps under `apps/*` to match domain concerns (calculators, airports, accounts, trips, search, core) and keep templates and URLs namespaced.  
In scope: app layout, import paths, template directories, namespaced URLs, shared `core/` helpers.  
Out of scope: specific model fields, specific calculations (covered by separate ADRs).

Project path note

- This ADR applies to the travelmathlite project. App roots live at `travelmathlite/apps/*`. Do not modify `blog_site/*` as part of this ADR or its briefs.

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

- Brief 01 (app scaffolding): 9b71cfb, e97bc83
- Brief 02 (settings wiring): 8099386
- Brief 03 (project URLs): a596919
- Brief 04 (templates organization): 6e6db00
- Brief 05 (tests): a8d8265
- Brief 06 (docs): 2fbb5aa
- Core→base rename (in-scope correction): f1ac883

All acceptance criteria verified; tests passing (14/14); documentation complete.

---

## Checklist seed

- [x] Namespaced URLs included
- [x] INSTALLED_APPS configured
- [x] Templates organized by app

---

## References

- PRD §4 Scope, §13 Traceability

---

## Appendix: Completion evidence (ADR-1.0.0)

### A.1 Acceptance criteria validation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| AC: `apps/*` directory exists with calculators, airports, accounts, trips, search, base (formerly core) | ✅ Done | Brief 01 — scaffolded all six apps under `travelmathlite/apps/` |
| AC: Each app has `urls.py` and templates under `templates/<app>/...` | ✅ Done | Brief 01 (URLs), Brief 04 (templates organization with partials) |
| AC: Project `urls.py` includes namespaced app URLs | ✅ Done | Brief 03 — all namespaces wired in `core/urls.py` |

### A.2 Implementation completion

| Task | Status | Evidence |
|------|--------|----------|
| Create `apps/*` with minimal `apps.py`, `urls.py`, `views.py`, `templates/` | ✅ Done | Brief 01 (commits: 9b71cfb, e97bc83) |
| Configure `INSTALLED_APPS` in settings | ✅ Done | Brief 02 (commit: 8099386) |
| Project `urls.py` includes app URLConfs under namespaces | ✅ Done | Brief 03 (commit: a596919) |

### A.3 Test validation

| Invariant/Test | Status | Evidence |
|----------------|--------|----------|
| INV-1: All URLs reverse via namespaces | ✅ Done | Brief 05 — tests validate `reverse('<app>:index')` for all apps |
| INV-2: Templates per app resolve without conflicts | ✅ Done | Brief 05 — tests assert template rendering with partials |
| Unit tests in `apps/*/tests.py` for URL reversing and template rendering | ✅ Done | Brief 05 (commit: a8d8265) — 14 tests, all passing |

### A.4 Documentation completion

| Doc | Status | Evidence |
|-----|--------|----------|
| Add `docs/architecture/app-layout.md` | ✅ Done | Brief 06 (commit: 2fbb5aa) |
| Update README with app structure | ✅ Done | Brief 06 — added "App layout (travelmathlite)" section |

### A.5 Checklist validation

| Item | Status |
|------|--------|
| Namespaced URLs included | ✅ Done |
| INSTALLED_APPS configured | ✅ Done |
| Templates organized by app | ✅ Done |

### Summary

All acceptance criteria, implementation steps, test invariants, and documentation requirements have been satisfied through Briefs 01–06. ADR-1.0.0 accepted on 2025-11-02.
