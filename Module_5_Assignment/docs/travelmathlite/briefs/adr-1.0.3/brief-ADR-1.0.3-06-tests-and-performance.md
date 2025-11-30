# BRIEF: Build nearest-airport tests & performance slice

Goal

- Add unit/behavioral tests and simple timing checks to validate ordering, unit handling, and performance targets, addressing PRD §4 F-002, §7 NF-001.

Scope (single PR)

- Files to touch: `apps/airports/tests_nearest.py` (new), optionally extend existing tests.
- Non-goals: UI polish; focus on coverage and timing evidence.

Standards

- Commits: conventional style (test/docs).
- Django TestCase; avoid external services.

Acceptance

- Unit tests: seed 5–10 airports around a coordinate; assert stable ordering (INV-1) and unit invariants.
- Timing evidence: log simple durations for `nearest()` on sample fixture (target p95 < 300 ms, local hint only).
- JSON/HTML view tests: response shape and codes; HTMX partial returns expected template.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [ ] Tests asserting:
  - [ ] Top 3 ordered by computed distance; distances attached
  - [ ] km/mi conversions correct
  - [ ] Country filter narrows results when provided
  - [ ] JSON endpoint returns `{results, count}`; HTML uses partial for HTMX
  - [ ] Timing log for nearest() on a small fixture (printed in test output)

Prompts for Copilot

- "Write tests to seed airports and verify nearest ordering and unit conversions."
- "Add tests for the JSON and HTML/HTMX endpoints. Include a simple timing capture and assert it is below a generous threshold in CI-safe manner or print only."

Summary

- Status: Planned — tests and timing evidence.
- Files: `apps/airports/tests_nearest.py` (plus any view/template tests).
- Tests: Ordering, units, filters, endpoints, timing.
- Issue: #TODO

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002; §7 NF-001
Requirements: FR-F-002-1, NF-001
