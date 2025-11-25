# BRIEF: Build nearest-airport views/API and URLs slice

Goal

- Implement views and API endpoints to expose nearest-airport results, addressing PRD §4 F-002, NF-001.

Scope (single PR)

- Files to touch: `apps/airports/views.py`, `apps/airports/urls.py`, optional `apps/airports/api.py` or DRF views if available.
- Non-goals: Form definitions (separate) and template layout (separate).

Standards

- Commits: conventional style (feat/test/docs).
- Prefer CBVs for pages; FBVs ok for lightweight JSON endpoints.
- Return top 3 results with distances and basic fields.

Acceptance

- User flow: Client submits query (city/IATA/coords) and receives top 3 nearest airports sorted by distance.
- HTML page route (GET+POST with form) and a JSON endpoint (GET with query params) both available.
- Response includes distance with unit (km/mi) and airport ident/iata/name.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [x] `NearestAirportView` (CBV) rendering a simple page with form and results
- [x] `nearest_airports_json` (FBV) returning JSON `{results:[{ident,iata,name,distance,unit}], count}`
- [x] URL patterns under `airports/` namespace; add link from base nav if not present
- [x] Tests for 200 responses, valid/invalid queries, and JSON payload shape

Prompts for Copilot

- "Add a CBV `NearestAirportView` that uses `NearestAirportForm` to resolve input and calls `Airport.objects.nearest(...)`."
- "Add a JSON endpoint that accepts `q`, `iso_country`, `unit`, `limit` and returns top results as JSON."
- "Write tests for GET/POST and JSON endpoint, including invalid inputs and proper HTTP codes."

Summary

- Status: Implemented — views/API endpoints and URLs complete.
- Files: `apps/airports/views.py`, `apps/airports/urls.py`, `apps/airports/templates/airports/nearest.html`, `apps/airports/tests/tests_views.py`.
- Tests: HTTP responses, JSON shape, ordering. All passing via `uv run`.
- Issue: #TODO

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002; §7 NF-001
Requirements: FR-F-002-1
