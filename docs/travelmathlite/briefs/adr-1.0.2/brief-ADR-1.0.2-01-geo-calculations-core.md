# BRIEF: Build geo calculations core slice

Goal

- Implement core geodesic/haversine distance calculations and unit conversions addressing PRD §4 F-001.

Scope (single PR)

- Files to touch: `apps/calculators/geo.py`, unit tests in `apps/calculators/tests.py`.
- Non-goals: Cost calculations, form integration, settings defaults.

Standards

- Commits: conventional style (feat/fix/docs/refactor/test/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).
- Type hints on new code; docstrings on public functions; PEP 8.

Acceptance

- User flow: Given two coordinates (lat/long), compute straight-line (geodesic) distance.
- Functions return distance in both km and miles.
- Unit conversion helpers for km ↔ miles.
- Heuristic driving distance formula: `driving_distance ≈ straight_line_km × route_factor`.
- Include migration? no
- Update docs & PR checklist.

Deliverables (Completed)

- [x] `calculators/geo.py` module with functions:
  - `haversine_distance(lat1, lon1, lat2, lon2) -> float` (returns km)
  - `geodesic_distance(lat1, lon1, lat2, lon2) -> float` (returns km, using geopy or similar)
  - `km_to_miles(km: float) -> float`
  - `miles_to_km(miles: float) -> float`
  - `estimate_driving_distance(straight_line_km: float, route_factor: float = 1.2) -> float`
- [x] Unit tests with known city pairs (e.g., NYC to LA)
- [x] Test invariant: conversions km ↔ miles are mathematically correct
- [x] Test edge cases: zero distance, same point, antipodal points

Prompts for Copilot

- "Generate a Python module `calculators/geo.py` with haversine and geodesic distance functions. Include type hints and docstrings. Use geopy if available, otherwise implement haversine formula directly."
- "Create Django TestCase for `geo.py` with tests for known city pairs (NYC to LA, London to Paris). Verify distance calculations within acceptable tolerance."
- "Add unit conversion helpers km_to_miles and miles_to_km with tests ensuring mathematical correctness."
- "Implement estimate_driving_distance function that applies a route factor to straight-line distance."
- "Propose commit messages for geo calculations core implementation."

Summary

- Status: Completed — core geodesic/haversine distance, unit conversions, and driving estimate delivered.
- Files: `apps/calculators/geo.py`, `apps/calculators/tests.py`.
- Tests: 24 tests passing at completion for this slice.
- Commits: [8991c6a](https://github.com/ahuimanu/CIDM6325/commit/8991c6a) (implementation), [4ec4480](https://github.com/ahuimanu/CIDM6325/commit/4ec4480) (brief completion update).
- Issue: #44.

---
ADR: adr-1.0.2-geo-calculation-methods.md
PRD: §4 F-001, FR-F-001-1
Issue: #44
