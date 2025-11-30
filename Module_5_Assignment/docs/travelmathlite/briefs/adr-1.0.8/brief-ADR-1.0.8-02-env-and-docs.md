```markdown
# BRIEF ADR-1.0.8-02: Env examples and docs

Goal

- Provide a `.env.example` and `docs/ops/settings.md` that document required env variables, local defaults, and how to validate prod settings.

Scope (single PR)

- Files to touch: `.env.example`, `docs/ops/settings.md`, small README note in project root.
- Non-goals: secrets management tooling (Vault), CI/CD secret injection.

Standards

- `.env.example` must list each required variable with a short comment and safe local defaults where appropriate (but never real secrets).
- Documentation must be concise, include example commands, and reference PRD/ADR links.

Acceptance

- `.env.example` contains at minimum: `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `EMAIL_URL`, `DJANGO_DEBUG` (optional), and `SENTRY_DSN` (optional).
- `docs/ops/settings.md` includes: how to run locally with `uv run`, how to test prod settings (import test or manage command), and what to check during review.

Prompts for Copilot

- "Create a `.env.example` with required variables and short inline comments describing each variable."
- "Draft `docs/ops/settings.md` explaining how to run locally, test prod settings, and common troubleshooting steps. Include sample commands."

Notes

- Keep example values safe for classroom use.  

```
