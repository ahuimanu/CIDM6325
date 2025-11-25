# BRIEF: Build test infrastructure and base classes slice

Goal

- Set up test infrastructure with base test classes, fixtures, and helpers addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/base/tests/__init__.py`, `travelmathlite/apps/base/tests/base.py`, `docs/travelmathlite/testing.md`.
- Behavior: Create reusable base TestCase classes, common fixtures, and helper methods for deterministic testing.
- Non-goals: Actual test implementation (separate briefs), CI configuration details.

Standards

- Commits: conventional style (feat/test/docs).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: Base test classes available for import across all apps; fixtures documented and reusable.
- Test helpers for mocking external calls and freezing time are available.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create a base TestCase class in `apps/base/tests/base.py` with common setup and helper methods for testing Django views and models."
- "Add fixture helpers for creating test data (e.g., users, airports) deterministically without external calls."
- "Document the test infrastructure in `docs/travelmathlite/testing.md` with examples of using base classes and fixtures."
- "Include helper methods for mocking external API calls and time-sensitive operations."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1, NF-004
Invariants: INV-1 (tests deterministic and isolated)
