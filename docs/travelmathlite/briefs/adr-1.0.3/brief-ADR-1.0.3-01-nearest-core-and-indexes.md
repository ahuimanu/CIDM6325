# BRIEF: Build nearest-airport core + indexes slice

Goal

- Implement nearest-airport lookup core (bounding box + haversine) and database indexes, addressing PRD §4 F-002/F-004, NF-001.

Scope (single PR)

- Files to touch: `apps/airports/models.py` (QuerySet helper, indexes), `apps/airports/migrations/*` (indexes), `apps/airports/tests_*.py` (ordering/unit tests).
- Non-goals: UI templates, forms, endpoints (separate briefs).

Standards

- Commits: conventional style (feat/fix/docs/refactor/test/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).
- Keep logic portable (SQLite-first; Postgres optional later).

Acceptance

- User flow: Given a coordinate (lat, lon), return top 3 nearest active airports ordered by distance.
- Query pre-filters via bounding box; final ordering by precise haversine.
- Distance units: always attach `distance_km` and optionally `distance_mi` when requested.
- Indexes exist for coordinate and common filters; migrations included.
- Include migration? yes (indexes)
- Update docs & PR checklist.

Deliverables

- [ ] `AirportQuerySet.nearest(lat, lon, limit=3, radius_km=..., iso_country=None, unit='km')`
- [ ] `_bounding_box_filters(lat, lon, radius_km)` helper
- [ ] DB indexes covering `(latitude_deg, longitude_deg)` and filters (`iso_country`, `active`)
- [ ] Unit tests verifying ordering, attached distances, and iso_country filter

Prompts for Copilot

- "Add a QuerySet method `nearest(...)` on `AirportQuerySet` that applies a bounding box filter, computes haversine for candidates, sorts by distance, and returns the top N. Attach `distance_km` (and `distance_mi` when requested)."
- "Create a migration adding composite index on `(latitude_deg, longitude_deg)` and individual indexes for `iso_country` and `active` if missing."
- "Write tests that seed 3–5 airports around a coordinate and assert the expected order and attached distance attributes."

Summary

- Status: Planned — core nearest-airport logic and indexes.
- Files: `apps/airports/models.py`, `apps/airports/migrations/*`, `apps/airports/tests_*.py`.
- Tests: ordering and distance attachment; country filter behavior.
- Issue: #TODO

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002, F-004; §7 NF-001
Requirements: FR-F-002-1, FR-F-004-1
