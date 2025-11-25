# BRIEF: Build HTMX-enhanced calculator forms slice

Goal

- Add HTMX attributes to calculator forms for partial updates addressing PRD §4 F-001 and F-003.

Scope (single PR)

- Files to touch: Calculator form templates (e.g., `apps/calculators/templates/calculators/distance.html`, `apps/calculators/templates/calculators/cost.html`), corresponding views.
- Behavior: Add `hx-post`, `hx-target`, `hx-swap` attributes to forms; ensure CSRF tokens are included; forms submit asynchronously when HTMX is available and synchronously otherwise.
- Non-goals: Partial template rendering (separate), view logic for detecting HTMX (separate).

Standards

- Commits: conventional style (feat/refactor).
- Forms must include CSRF tokens via `{% csrf_token %}`.
- Preserve standard POST behavior for non-HTMX requests (progressive enhancement).

Acceptance

- User flow: Calculator forms have `hx-post` to their action URL, `hx-target` pointing to result container, `hx-swap="outerHTML"` or similar.
- CSRF tokens present in all forms.
- Forms submit normally when JS disabled.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add HTMX attributes to calculator forms: `hx-post='{% url ... %}'`, `hx-target='#result-container'`, `hx-swap='outerHTML'`."
- "Verify CSRF token is present in form with `{% csrf_token %}`."
- "Ensure forms degrade gracefully: action attribute set, method='POST', submit button accessible."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §4 F-001, F-003
Requirements: FR-F-001-2, FR-F-003-1
