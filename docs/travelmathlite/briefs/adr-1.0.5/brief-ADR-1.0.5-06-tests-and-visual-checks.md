# BRIEF: Build tests and visual checks for HTMX slice

Goal

- Add unit and behavioral tests for HTMX forms and partial rendering addressing PRD §10 Acceptance.

Scope (single PR)

- Files to touch: `apps/calculators/tests/test_views.py`, Playwright visual check script under `travelmathlite/scripts/`, screenshot output folder.
- Behavior: Test HTMX request detection, partial template rendering, CSRF token presence, and full-page fallback. Add visual check script to capture HTMX interaction (submit form, verify result swap).
- Non-goals: Performance testing, load testing, fuzzing.

Standards

- Commits: conventional style (test/docs/chore).
- Use Django TestCase with RequestFactory for view tests.
- Use Playwright for headless visual check; store screenshots under `travelmathlite/screenshots/calculators/`.

Acceptance

- Tests cover: HTMX header detection, partial vs. full template selection, CSRF token in responses, validation errors in both flows.
- Visual check script captures HTMX form submission and result swap.
- Non-JS fallback verified (full page reload works).
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Write Django tests using RequestFactory to simulate HTMX and non-HTMX POST requests; verify correct template selection."
- "Add tests for CSRF token presence in both full and partial responses."
- "Create Playwright script to navigate to calculator, fill form, submit with HTMX, and capture screenshot of updated result."
- "Document test approach and visual check usage in `docs/ux/htmx-patterns.md`."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §10 Acceptance
Requirements: FR-F-001-2, FR-F-003-1
Invariants: INV-1, INV-2
