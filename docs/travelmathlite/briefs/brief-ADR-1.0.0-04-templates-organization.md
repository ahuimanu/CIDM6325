# BRIEF: ADR-1.0.0 — Templates organization by app

Goal

- Organize templates under per-app directories and verify includes resolve without conflicts.

Scope (single PR)

- For each app, create `templates/<app>/` and add a minimal `index.html` and `base_<app>.html` or reuse global base.
- Adopt standard include paths to avoid collisions (e.g., `templates/<app>/partials/...`).
- Non-goals: full base layout (covered by UI stack ADR).

Standards

- Lint and format with Ruff; conventional commits.
- Autoescape remains enabled.

Acceptance

- Each app renders its `index.html` with `{% extends 'base.html' %}` or app base; includes resolve.
- No template name collisions across apps.

Prompts for Copilot

- "Create per-app templates with minimal content and an include to demonstrate resolution."
- "Show how to name partials to prevent collisions and update includes accordingly."

Traceability

- ADR: ADR-1.0.0 (§Requirements binding, FR-F-007-1; INV-2).
- PRD: §4 Scope (F-007), §13 Traceability.
