# BRIEF: Build partial templates for HTMX responses slice

Goal

- Create partial templates for calculator results that can be returned in HTMX responses addressing PRD §4 F-001 and F-003.

Scope (single PR)

- Files to touch: New partial templates under `apps/calculators/templates/calculators/partials/` (e.g., `distance_result.html`, `cost_result.html`), shared blocks if needed.
- Behavior: Partials contain only the result fragment (e.g., result card, errors, success message); reuse validation display logic from full templates.
- Non-goals: View logic for detecting HTMX (separate), form attributes (separate).

Standards

- Commits: conventional style (feat/refactor).
- Use Django template includes and blocks to avoid duplication between full and partial templates.
- Partials must be self-contained HTML fragments suitable for `hx-swap`.

Acceptance

- User flow: Each calculator has a partial template that renders just the result region.
- Partials share validation/error display code with full templates via includes or blocks.
- Partials include proper ARIA attributes and focus hints for accessibility.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create partial templates under `apps/calculators/templates/calculators/partials/` for distance and cost results."
- "Extract result rendering logic into reusable blocks or includes shared between full and partial templates."
- "Add `id` attributes to result containers for HTMX targeting (e.g., `id='result-container'`)."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §4 F-001, F-003; §7 NF-002
Requirements: FR-F-001-2, FR-F-003-1, NF-002
