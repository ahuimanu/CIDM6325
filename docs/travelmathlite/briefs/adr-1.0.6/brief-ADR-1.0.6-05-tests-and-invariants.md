# BRIEF: Tests for model pruning, session migration, and per-user access

Goal

- Add Django `TestCase` coverage for `SavedCalculation` pruning (max 10), session migration after login, and per-user access control on list/delete views.

Scope (single PR)

- Files to touch: `apps/trips/tests/test_saved_calculation.py`, `apps/accounts/tests/test_session_migration.py`, `apps/trips/tests/test_views_saved.py`.
- Behavior: Unit tests for model create+prune; signal-driven migration behavior; view tests for authenticated filtering and delete permissions.
- Non-goals: Playwright or UI screenshots (optional in separate PR).

Standards

- Commits: conventional (test); include Issue reference.
- Use `uv run` to execute tests; do not add pytest; keep tests deterministic.

Acceptance

- Tests prove INV-1 (privacy) and INV-2 (cap at 10) hold.
- Session migration test validates safe behavior when no session data present.
- View tests ensure non-owners cannot see/delete others' items.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Write tests that create 11 `SavedCalculation` entries for one user and assert count==10 with oldest removed."
- "Test `user_logged_in` receiver: seed session keys, authenticate a user, assert keys migrated/cleaned and no DB rows created until next submission."
- "Write view tests for list and delete: owner vs non-owner behaviors; 404/403 as appropriate."

---
ADR: adr-1.0.6-auth-and-saved-calculations-model.md
PRD: §4 F-006; §7 NF-003
Requirements: FR-F-006-1, NF-003; Invariants: INV-1, INV-2
