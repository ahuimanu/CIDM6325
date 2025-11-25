# BRIEF: Build HTMX base template integration slice

Goal

- Add HTMX library to base template and configure basic progressive enhancement setup addressing PRD §4 F-001, F-003, and NF-002.

Scope (single PR)

- Files to touch: `travelmathlite/templates/base.html` (or equivalent base template), optional documentation in `docs/ux/htmx-patterns.md`.
- Behavior: Include HTMX CDN link in base template head; verify HTMX is available globally; add any base HTMX configuration needed.
- Non-goals: Form-specific HTMX attributes (separate), partial templates (separate), view logic changes.

Standards

- Commits: conventional style (feat/docs).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: HTMX library loaded on all pages; can be verified via browser console `typeof htmx !== 'undefined'`.
- Templates remain valid HTML5; no-JS users see no broken functionality.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add HTMX CDN link to `templates/base.html` in the head section; use latest stable version from unpkg or CDN."
- "Create placeholder documentation in `docs/ux/htmx-patterns.md` explaining progressive enhancement approach and HTMX configuration."
- "Ensure CSP compatibility if Content-Security-Policy headers are configured."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §4 F-001, F-003, F-007; §7 NF-002
Requirements: FR-F-001-2, FR-F-003-1, NF-002
