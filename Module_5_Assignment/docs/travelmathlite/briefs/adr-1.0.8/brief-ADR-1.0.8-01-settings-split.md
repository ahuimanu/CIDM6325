# BRIEF ADR-1.0.8-01: Settings split (base/local/prod)

Goal

- Implement the settings split into `base`, `local`, and `prod` modules per ADR-1.0.8 decision.

Scope (single PR)

- Files to touch:
  - `project/settings/base.py` (common settings)
  - `project/settings/local.py` (development overrides)
  - `project/settings/prod.py` (production hardening)
  - `manage.py` and `wsgi.py` if necessary for examples (read-only changes preferred)
- Non-goals: container-specific deployment files, infra provisioning.

Standards

- Keep code PEP8; add type hints in new helper utilities if any.
- Use `django-environ` for env parsing; import it in `base.py` and document usage.
- Add docstring to each settings module describing its purpose.

Acceptance

- `base.py` contains all shared settings and reads env vars via `env = environ.Env()` with sensible defaults.
- `local.py` imports from `base` and sets `DEBUG=True`, local DB defaults, and developer tools comments.
- `prod.py` imports from `base`, sets `DEBUG=False` by default, and enforces presence of `SECRET_KEY` and `ALLOWED_HOSTS` (raise on missing required envs).
- Add a small unit test that imports each settings module and asserts expected DEBUG values.

Prompts for Copilot

- "Create `base.py`, `local.py`, and `prod.py` skeletons that clearly show where to put env-driven overrides and security settings."
- "Provide a small import-based test for `DEBUG` state in each settings variant using Django TestCase or simple import assertions."

Notes

- Keep file-level changes minimal and reviewable (<300 lines).  

