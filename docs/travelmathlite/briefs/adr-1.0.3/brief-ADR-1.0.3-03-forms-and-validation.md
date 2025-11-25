# BRIEF: Build nearest-airport forms & validation slice

Goal

- Implement input forms to accept city, IATA, or lat,lon and normalize to coordinates, addressing PRD §4 F-002/F-004.

Scope (single PR)

- Files to touch: `apps/airports/forms.py`, unit tests for forms.
- Non-goals: Views/endpoints and templates (covered elsewhere).

Standards

- Commits: conventional style (feat/test/docs).
- Django tests: use Django TestCase.
- Reuse existing airports model/lookup where possible.

Acceptance

- User flow: User enters a city, IATA code, or coordinates; form resolves to (lat, lon) with optional country filter.
- Validation: coordinate range checks; IATA format; city/airport lookups; helpful errors.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [x] `NearestAirportForm` with fields:
  - [x] `query` (city name | IATA | "lat,lon")
  - [x] `iso_country` (optional)
  - [x] `unit` (km/mi)
  - [x] `limit` (default 3; max 10)
- [x] Clean methods normalize to coords, set `resolved_coords`
- [x] Tests for valid/invalid inputs; normalization and defaults

Prompts for Copilot

- "Create `NearestAirportForm` resolving input to coordinates (lat,lon). Support city (via airports.City/municipality), IATA (via Airport.iata_code), or direct lat,lon."
- "Validate ranges and formats; write tests covering happy paths and failures."

Summary

- Status: Implemented — forms and validation complete.
- Files: `apps/airports/forms.py`, `apps/airports/tests/tests_forms.py`.
- Tests: form normalization, validation, and defaults.
- Issue: #TODO

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002, F-004
Requirements: FR-F-004-1
