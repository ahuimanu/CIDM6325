# BRIEF: Build Playwright visual check integration with tests slice

Goal

- Integrate Playwright visual checks alongside unit tests for optional behavioral validation addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/scripts/visual_check.py`, `docs/travelmathlite/testing.md`, optional test runner script.
- Behavior: Visual checks run independently of unit tests; capture screenshots for major flows (calculators, search).
- Non-goals: Replacing unit tests with Playwright, full E2E test suite.

Standards

- Commits: conventional style (feat/test/docs).
- Use `uvx playwright` for running scripts; lint/format with Ruff.
- Django tests: use Django TestCase for unit tests; Playwright for visual checks (no pytest).

Acceptance

- User flow: Run `uvx playwright` script to capture screenshots; run `uv run python manage.py test` for unit tests independently.
- Visual check script documented in `scripts/README.md` and `docs/travelmathlite/testing.md`.
- Screenshots stored under `travelmathlite/screenshots/` or feature-specific directory.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Update `travelmathlite/scripts/visual_check.py` to capture screenshots of calculator and search flows."
- "Ensure Playwright script can run headless and store screenshots in `screenshots/` directory."
- "Document how to run visual checks in `docs/travelmathlite/testing.md` with example commands."
- "Add optional integration: run visual checks after unit tests pass (document pattern)."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated)
