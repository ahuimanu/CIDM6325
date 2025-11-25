# Copilot Brief: ADR-1.0.0-03 Project URLs and Namespacing

## Goal
Include per-app URLConfs under namespaces in the project `urls.py` to enable reliable reverse() usage.

## Scope
- Create/confirm `apps/*/urls.py` define `app_name` and at least an index route.
- Update project `urls.py` to include all app URLs under namespaces.
- Non-goals: content of views beyond trivial index pages.

## Standards
- Use `uv run` to run checks; format/lint with Ruff.
- Conventional commits.

## Acceptance
- `reverse('calculators:index')` and peers resolve.
- Project `urls.py` includes all app URLs under namespaces; Django checks pass.

## Prompts for Copilot
- Add namespaced includes for all domain apps and prove reverse() works with a small smoke test.
- Generate minimal index views and templates for each app to validate urlconf wiring.

---
ADR: ADR-1.0.0
PRD: §4 Scope, §13 Traceability
