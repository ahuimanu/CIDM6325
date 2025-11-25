# BRIEF: Build mocking and time-freezing test examples slice

Goal

- Create example tests demonstrating mocking external calls and time-sensitive operations addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/base/tests/test_mocking_examples.py`, `docs/travelmathlite/testing.md`.
- Behavior: Provide reusable patterns for mocking HTTP requests, database queries, and freezing time for deterministic tests.
- Non-goals: Comprehensive mocking library (use stdlib unittest.mock), third-party time libraries (freezegun optional).

Standards

- Commits: conventional style (test/docs).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase and unittest.mock (no pytest).

Acceptance

- User flow: Developers can reference example tests for mocking patterns.
- Documentation updated with mocking and time-freezing examples.
- Examples cover: mocking external HTTP calls, mocking timezone-aware operations.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create example tests in `apps/base/tests/test_mocking_examples.py` demonstrating unittest.mock for HTTP requests."
- "Add examples of mocking Django model methods and external API calls."
- "Show how to freeze time using unittest.mock or freezegun (if adopted) for deterministic date/time tests."
- "Update `docs/travelmathlite/testing.md` with mocking patterns and best practices; include code snippets."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated; no real network calls)
