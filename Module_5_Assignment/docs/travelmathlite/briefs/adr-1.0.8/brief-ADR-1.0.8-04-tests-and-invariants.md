```markdown
# BRIEF ADR-1.0.8-04: Tests and invariants

Goal

- Add tests and verification steps to ensure settings invariants (INV-1 and INV-2) and provide guidance for reviewers.

Scope (single PR)

- Files to touch: `apps/*/tests/` (new small test modules), `docs/ops/settings.md` (test steps), and possibly a management command for quick checks (optional).
- Non-goals: full integration or deployment tests.

Standards

- Use Django `TestCase` for unit tests.
- Tests should be lightweight and fast.

Acceptance

- Tests verify that importing `project.settings.prod` sets `DEBUG=False` and that security-related settings (cookie flags, middleware) are present.
- A reviewer checklist entry is added to `docs/ops/settings.md` documenting manual validation steps.

Prompts for Copilot

- "Write a Django TestCase that imports `project.settings.prod` and asserts `DEBUG is False` and that `SESSION_COOKIE_SECURE` is True (or properly configured)."
- "Optionally provide a small management command `check_settings` that prints key settings values for manual inspection."

Notes

- Keep tests deterministic; avoid reading the real environment during test run (use monkeypatch or temp env settings when needed).

```
