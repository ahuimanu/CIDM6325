# BRIEF: Build calculator view and form tests slice

Goal

- Implement tests for calculator views and forms using RequestFactory addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/calculators/tests/test_views.py` or extend `travelmathlite/apps/calculators/tests.py`.
- Behavior: Test view logic, form validation, success/error rendering; use RequestFactory for request simulation.
- Non-goals: Browser-based testing (use Playwright scripts separately), unit logic tests (separate brief).

Standards

- Commits: conventional style (test).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase and RequestFactory (no pytest).

Acceptance

- User flow: Run `uv run python manage.py test calculators` and see view tests pass.
- Tests cover GET requests, valid POST submissions, invalid form data handling.
- HTMX request detection tested (HX-Request header present/absent).
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create view tests in `apps/calculators/tests/test_views.py` using RequestFactory to test calculator form views."
- "Test GET requests return correct templates and context; POST requests with valid data process correctly."
- "Add tests for form validation errors and error message rendering."
- "Test HTMX request detection: verify views return partials when HX-Request header is present, full templates otherwise."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated), INV-2 (same view handles HTMX and full-page)
