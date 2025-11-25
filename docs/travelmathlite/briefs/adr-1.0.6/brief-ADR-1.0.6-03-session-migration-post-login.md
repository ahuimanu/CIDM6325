# BRIEF: Migrate anonymous session inputs after login

Goal

- When a user logs in, migrate any anonymous session-stored calculator inputs to the user context so the next calculation saves properly (PRD §4 F-006; NF-003 privacy and correctness).

Scope (single PR)

- Files to touch: a small helper in `apps/calculators/session.py` or `apps/core/session.py`, and a post-login hook via `user_logged_in` signal receiver in `apps/accounts/signals.py` (or middleware alternative if preferred).
- Behavior: On `user_logged_in`, read expected session keys for last calculator inputs, copy to a user-associated benign store (or simply leave in session but mark as user-bound), and clear any PII. Do not auto-create `SavedCalculation` yet; defer until the user actually submits the next calculation.
- Non-goals: Saved list UI; model creation logic.

Standards

- Commits: conventional (feat); include Issue reference.
- Keep data minimal; no sensitive info in session; adhere to Django session security practices.

Acceptance

- After login, the next calculator submission by the user has access to prior anonymous inputs.
- No errors if no session data present; idempotent and safe to run multiple times.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add `user_logged_in` signal receiver in `apps/accounts/signals.py` to migrate anonymous calculator input keys from session to a user-ready state; avoid creating DB rows during login."
- "Create a tiny `session.py` helper to encapsulate session key names and safe read/write/delete operations."
- "Wire signals in `apps/accounts/apps.py` AppConfig `ready()` and ensure app is installed."

---
ADR: adr-1.0.6-auth-and-saved-calculations-model.md
PRD: §4 F-006; §7 NF-003
Requirements: FR-F-006-1, NF-003; Invariants: INV-1
