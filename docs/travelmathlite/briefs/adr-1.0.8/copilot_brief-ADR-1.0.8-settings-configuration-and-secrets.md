```markdown
# BRIEF: Build Settings configuration & secrets slice

Goal

- Implement settings split and secrets configuration addressing PRD §4 F-012 and NF-003.

Scope (single PR)

- Files to touch: `project/settings/base.py`, `project/settings/local.py`, `project/settings/prod.py`, `.env.example`, `docs/ops/settings.md`, minimal README updates.
- Non-goals: container provisioning, deployment scripts, changes to DB schema.

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets committed to repo; supply `.env.example` only.
- Use `django-environ` for env parsing.
- Django tests: use `unittest/Django TestCase` (no pytest).

Acceptance

- User flow: Running locally uses `local` settings with `DEBUG=True` by default; running with `DJANGO_SETTINGS_MODULE=<project>.settings.prod` sets `DEBUG=False` and requires `ALLOWED_HOSTS`.
- Include migration? no
- Update docs & PR checklist: update `docs/ops/settings.md` and top-level README mention.

Prompts for Copilot

- "Generate `project/settings/base.py`, `local.py`, and `prod.py` skeletons using `django-environ` with documented required env vars (SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS, EMAIL_URL)."
- "Create a `.env.example` file listing required env variables and sensible local defaults for dev."
- "Write a short `docs/ops/settings.md` that explains how to run locally and how to test prod settings behavior."

```
