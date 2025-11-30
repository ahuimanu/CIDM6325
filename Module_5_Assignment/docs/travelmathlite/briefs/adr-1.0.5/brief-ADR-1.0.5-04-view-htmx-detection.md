# BRIEF: Build view HTMX detection and partial rendering slice

Goal

- Update calculator views to detect HTMX requests and return partial templates addressing PRD §4 F-001 and F-003.

Scope (single PR)

- Files to touch: Calculator views (e.g., `apps/calculators/views.py`), existing view logic.
- Behavior: Detect HTMX via `HX-Request` header; if HTMX, render partial template; otherwise, render full page. Reuse the same view for both flows (INV-1 from ADR).
- Non-goals: Template creation (separate), form attributes (separate), new validation logic.

Standards

- Commits: conventional style (feat/refactor).
- Use Django's `request.headers.get('HX-Request')` to detect HTMX.
- Maintain single view for both HTMX and full-page requests (no duplication).
- Django tests: use Django TestCase with `RequestFactory` to simulate both request types.

Acceptance

- User flow: Views return partial template when `HX-Request` header present; full template otherwise.
- Same validation, form processing, and business logic for both flows.
- Tests cover both HTMX and non-HTMX requests.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Update calculator views to check `request.headers.get('HX-Request')` and conditionally render partial template."
- "Preserve existing form processing and validation; only change template selection based on HTMX detection."
- "Add RequestFactory tests for both HTMX (`HX-Request: true`) and standard POST requests."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §4 F-001, F-003
Requirements: FR-F-001-2, FR-F-003-1
Invariants: INV-1 (same view for both flows), INV-2 (CSRF tokens present)
