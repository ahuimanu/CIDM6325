# BRIEF: Add SavedCalculation model and admin

Goal

- Implement `SavedCalculation` storing a user’s last 10 calculator runs with inputs/outputs JSON and housekeeping to cap entries (PRD §4 F-006).

Scope (single PR)

- Files to touch: `apps/trips/models.py`, `apps/trips/admin.py`, migration under `apps/trips/migrations/`.
- Behavior: Model fields: `user` (FK to `auth.User`), `calculator_type` (CharField), `inputs` (TextField JSON), `outputs` (TextField JSON), `created_at` (DateTimeField auto_add). Manager or model method enforces max 10 per user by pruning oldest on create.
- Non-goals: Views/templates; session migration.

Standards

- Commits: conventional (feat); include Issue reference.
- Use `uv run` for makemigrations/migrate; Ruff for lint/format.
- JSON storage: TextField with serialized JSON for portability; keep schema small.

Acceptance

- Migration creates `SavedCalculation` with fields above.
- Creating 11th item for a user prunes oldest so only 10 remain.
- Admin registration allows per-user list/search by `calculator_type` and date.
- Include migration? yes (one logical change)
- Update docs & PR checklist.

Prompts for Copilot

- "Define `SavedCalculation` in `apps/trips/models.py` with pruning logic in a custom manager or `save()`. Keep max 10 per user, delete oldest records when exceeding."
- "Register model in `apps/trips/admin.py` with list display of user, calculator_type, created_at, and search fields."
- "Generate and run migration using `uv run python manage.py makemigrations trips` and `migrate`."

---
ADR: adr-1.0.6-auth-and-saved-calculations-model.md
PRD: §4 F-006; §7 NF-003
Requirements: FR-F-006-1, NF-003; Invariants: INV-2
