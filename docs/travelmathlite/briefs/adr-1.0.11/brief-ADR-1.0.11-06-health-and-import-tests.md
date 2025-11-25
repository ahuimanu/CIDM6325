# BRIEF: Build health endpoint and data import tests slice

Goal

- Implement tests for health endpoint and data import/update operations addressing PRD §4 F-011 and NF-004.

Scope (single PR)

- Files to touch: `travelmathlite/apps/core/tests/test_health.py`, `travelmathlite/apps/airports/tests/test_import.py` (or equivalent).
- Behavior: Test health check endpoint returns correct status; test data import is idempotent and handles errors.
- Non-goals: Full CI pipeline config (separate), performance benchmarks.

Standards

- Commits: conventional style (test).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: Run `uv run python manage.py test core.tests.test_health` and see health tests pass.
- Health endpoint test verifies 200 status and correct JSON response.
- Import tests verify idempotent behavior (re-importing same data doesn't duplicate).
- Mock network downloads in import tests.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create tests in `apps/core/tests/test_health.py` for the health endpoint; verify it returns 200 status and expected JSON."
- "Create import tests in `apps/airports/tests/test_import.py` that mock network downloads and verify idempotent import behavior."
- "Test that re-importing the same dataset doesn't create duplicate records."
- "Add error handling tests for import operations (e.g., corrupted file, network failure)."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1, NF-004
Invariants: INV-1 (tests deterministic and isolated; no real network calls)
