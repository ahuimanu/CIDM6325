# BRIEF: ADR-1.0.0 — App scaffolding under `apps/*`

Goal

- Scaffold domain apps to establish clear boundaries per ADR-1.0.0.

Scope (single PR)

- Create `apps/` modules: calculators, airports, accounts, trips, search, core.
- Each app: `__init__.py`, `apps.py`, `urls.py`, `views.py`, `templates/<app>/` with a minimal index template.
- Non-goals: model fields, business logic (handled in other ADRs).

Standards

- Commits: conventional style (feat/docs/chore).
- Use `uv run` / `uvx`; lint+format with Ruff; no pytest (use Django TestCase if tests included).
- Namespaces: app `name` in `apps.py` and `app_name` in `urls.py`.

Acceptance

- `apps/*` directory exists for calculators, airports, accounts, trips, search, core.
- Each app has a `urls.py` exposing a trivial index route and a minimal template under `templates/<app>/index.html`.
- Repo lints clean (Ruff) and imports resolve.

Prompts for Copilot

- "Generate Django app scaffolds under apps/{app_name} with apps.py, urls.py (namespace), views.py (Index view), and templates/{app_name}/index.html."
- "Update __all__ and import paths if needed, preserving PEP 8."
- "Propose commit messages for each app scaffold in conventional style."

Traceability

- ADR: ADR-1.0.0 Application architecture and app boundaries (§Implementation outline).
- PRD: §4 Scope, §13 Traceability.
