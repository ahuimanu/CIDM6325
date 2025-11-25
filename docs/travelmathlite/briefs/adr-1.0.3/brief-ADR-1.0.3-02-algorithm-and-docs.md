# BRIEF: Build nearest-airport algorithm documentation slice

Goal

- Document nearest-airport algorithm (bounding box prefilter + haversine) addressing PRD §4 F-002, §7 NF-001.

Scope (single PR)

- Files to touch: `docs/travelmathlite/algorithms/nearest-airport.md`.
- Non-goals: App code changes; focus on docs with formulas, examples, and limitations.

Standards

- Commits: conventional style (docs).
- Clear explanations for non-technical readers; include formulas and examples.

Acceptance

- User flow: Reader understands method, defaults, and trade-offs (SQLite-first portability).
- Document includes: bounding box derivation, haversine formula, example query, unit handling, performance notes.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [x] `docs/travelmathlite/algorithms/nearest-airport.md` with:
  - [x] Bounding box derivation and lat/lon deltas from radius
  - [x] Haversine formula and constants
  - [x] Example: coordinate → top 3 airports (with distances)
  - [x] Unit handling (km, mi) and conversion
  - [x] Limitations; perf targets (p95 < 300 ms on sample dataset)
  - [x] Index usage and SQLite rationale

Prompts for Copilot

- "Generate `docs/travelmathlite/algorithms/nearest-airport.md` explaining the bounding box + haversine approach. Include equations, rationale, an example, and limitations."
- "Add a note about index usage and why this works well on SQLite without PostGIS."

Summary

- Status: Complete — algorithms doc finished.
- Files: `docs/travelmathlite/algorithms/nearest-airport.md`.
- Tests: N/A (documentation).
- Issue: #51 (to be created)

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002; §7 NF-001
Requirements: FR-F-002-1
