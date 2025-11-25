# BRIEF: Build authentication and authorization tests slice

Goal

- Implement tests for authentication flows and permission checks addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/core/tests/test_auth.py` or relevant app tests.
- Behavior: Test login, logout, registration (if applicable), and access control to protected views.
- Non-goals: OAuth/SSO integration (if not in scope), password reset flows (unless specified).

Standards

- Commits: conventional style (test).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: Run `uv run python manage.py test` and see auth tests pass.
- Tests cover authenticated vs. anonymous access, login/logout flows, permission-based view access.
- Mock external auth providers if applicable.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create authentication tests in `apps/core/tests/test_auth.py` for login and logout views."
- "Test that protected views require authentication and redirect anonymous users."
- "Add tests for user registration (if applicable) with valid and invalid form submissions."
- "Verify permission checks: users without required permissions receive 403 or redirect."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated)
