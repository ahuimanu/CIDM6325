# Copilot Brief: ADR-1.0.0-01 App Scaffolding

## Goal
Scaffold domain apps to establish clear boundaries per ADR-1.0.0.

## Scope
- Create app packages under `travelmathlite/apps/*`: calculators, airports, accounts, trips, search, core.
- Each app: `__init__.py`, `apps.py`, `urls.py`, `views.py`, `templates/<app>/index.html`.
- Non-goals: model fields, business logic.

## Standards
- PEP 8, docstrings, type hints on new code.
- Conventional commits (feat/docs/chore).
- Use `uv run` / `uvx`; lint+format with Ruff; Django TestCase for tests.

## Acceptance
- `travelmathlite/apps/*` directory exists for all domain apps.
- Each app has a namespaced `urls.py` and minimal template.
- Repo lints clean and imports resolve.

## Prompts for Copilot
- Generate Django app scaffolds under apps/{app_name} with apps.py, urls.py, views.py, and templates/{app_name}/index.html.
- Propose commit messages for each app scaffold in conventional style.

---
ADR: ADR-1.0.0 Application architecture and app boundaries
PRD: §4 Scope, §13 Traceability
