# BRIEF: ADR-1.0.0 — Settings wiring (INSTALLED_APPS, templates)

Goal

- Wire domain apps into settings and ensure template resolution supports per-app templates.

Scope (single PR)

- Add `apps.calculators`, `apps.airports`, `apps.accounts`, `apps.trips`, `apps.search`, `apps.core` to `INSTALLED_APPS`.
- Ensure `TEMPLATES['OPTIONS']['loaders']` and `APP_DIRS` support per-app templates (default behavior).
- Add project-level templates dir if needed (e.g., `templates/`).
- Non-goals: prod split (covered by settings ADR), business logic.

Standards

- Use `uv run` / `uvx`; format/lint with Ruff.
- Conventional commits; no secrets in repo.

Acceptance

- All apps import without errors; manage.py check passes.
- Templates under `templates/<app>/` resolve via `{% include %}` and `render`.

Prompts for Copilot

- "Update settings to include new domain apps; confirm APP_DIRS or loaders handle per-app templates."
- "Add a minimal project-level `templates/` and verify resolution with a smoke test."

Traceability

- ADR: ADR-1.0.0 (§Implementation outline: settings wiring).
- PRD: §4 Scope.
