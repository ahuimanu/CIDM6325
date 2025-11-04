# Copilot Brief: ADR-1.0.0-02 Settings Wiring (INSTALLED_APPS, Templates)

## Goal
Wire domain apps into settings and ensure template resolution supports per-app templates.

## Scope
- Add all domain apps to `INSTALLED_APPS`.
- Ensure template loaders and APP_DIRS support per-app templates.
- Add project-level templates dir if needed.
- Non-goals: prod split, business logic.

## Standards
- Use `uv run` / `uvx`; format/lint with Ruff.
- Conventional commits; no secrets in repo.

## Acceptance
- All apps import without errors; manage.py check passes.
- Templates under `templates/<app>/` resolve via `{% include %}` and `render`.

## Prompts for Copilot
- Update settings to include new domain apps; confirm template resolution.
- Add a minimal project-level `templates/` and verify resolution with a smoke test.

---
ADR: ADR-1.0.0
PRD: §4 Scope
