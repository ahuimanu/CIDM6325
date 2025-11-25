# BRIEF: Build nearest-airport templates & HTMX slice

Goal

- Implement minimal UI templates (and HTMX partials if desired) to display nearest-airport results, addressing PRD §4 F-002.

Scope (single PR)

- Files to touch: `apps/airports/templates/airports/nearest.html`, `apps/airports/templates/airports/partials/nearest_results.html`.
- Non-goals: Algorithm or form logic.

Standards

- Commits: conventional style (feat/docs/test).
- Use existing base layout; add navigation link if missing.
- Keep markup simple and accessible; no JS frameworks.

Acceptance

- User flow: Page shows a form and renders top 3 results sorted by distance (unit-aware).
- HTMX: POST updates results div without full refresh when `HX-Request` header present.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [ ] `airports/nearest.html` (extends base; includes form and results target container)
- [ ] `airports/partials/nearest_results.html` (loop results with distance and links)
- [ ] Nav link to Nearest Airports page from base template
- [ ] Template tests (rendering, includes, partial usage)

Prompts for Copilot

- "Create `nearest.html` with a form posting to the nearest view, and an HTMX target for results."
- "Add partial template `partials/nearest_results.html` that lists top 3 with distance and unit."
- "Add tests that GET renders, POST/HTMX returns partial, and nav link is present."

Summary

- Status: Planned — templates/partials and light HTMX wiring.
- Files: `apps/airports/templates/airports/nearest.html`, `apps/airports/templates/airports/partials/nearest_results.html`, `apps/airports/tests_templates.py`.
- Tests: Template rendering and HTMX partial behavior.
- Issue: #TODO

---
ADR: adr-1.0.3-nearest-airport-lookup-implementation.md
PRD: §4 F-002
Requirements: FR-F-002-1
