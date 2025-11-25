# Copilot Brief: ADR-1.0.0-05 Tests for URL Reverse and Template Rendering

## Goal
Add unit tests to enforce invariants: namespaced URL reversing works and templates resolve per app.

## Scope
- In each app, add tests for `reverse('<app>:index')` and simple render of `index.html`.
- Optionally add a shared test module to assert all namespaces exist.
- Non-goals: business logic tests.

## Standards
- Use Django TestCase. Run via `uv run python manage.py test`.
- Keep tests deterministic and fast.

## Acceptance
- Tests pass verifying reverse and render per app.
- CI/local run includes these tests and shows green.

## Prompts for Copilot
- Generate Django TestCase that verifies reverse('{app_namespace}:index') works and renders the expected template.
- Add a small shared test that iterates expected app namespaces and asserts they reverse.

---
ADR: ADR-1.0.0
PRD: §4 Scope (FR-F-007-1/FR-F-008-1), §11 Success metrics
