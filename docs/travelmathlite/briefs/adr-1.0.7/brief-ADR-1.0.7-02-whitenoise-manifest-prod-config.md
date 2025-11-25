# BRIEF: Enable Manifest storage and WhiteNoise in production

Goal

- Adopt `ManifestStaticFilesStorage` plus WhiteNoise middleware so hashed filenames are produced during `collectstatic` and served directly by the Django process in demo/prod environments (PRD §4 F-010; §7 NF-004).

Scope (single PR)

- Files to touch: `travelmathlite/core/settings.py`, `travelmathlite/core/wsgi.py`, `pyproject.toml` (add `whitenoise` dependency), deployment docs/scripts invoking `collectstatic`.
- Tasks: conditionally set `STATICFILES_STORAGE="django.contrib.staticfiles.storage.ManifestStaticFilesStorage"` (enabled when `DEBUG=False` or via env flag), add `WhiteNoiseMiddleware` after `SecurityMiddleware`, configure `WHITENOISE_MAX_AGE`, compression, and immutable file serving; update `uv run manage.py collectstatic` instructions for CI.
- Non-goals: CDN/front-door configs, caching headers for media uploads (covered later).

Standards

- Commits: conventional (`feat/chore/docs`) with Issue refs.
- Use `uv run python manage.py collectstatic --noinput` before pushing; capture transcript for ADR evidence.
- Tests rely on Django `TestCase`; add targeted setting tests if needed (no pytest).

Acceptance

- WhiteNoise installed and middleware stack order documented; `python -m whitenoise.runserver` not required.
- `collectstatic` emits hashed filenames and `staticfiles.json`; template references resolve hashed URLs automatically when `DEBUG=False` (verified via shell test or integration test).
- Local dev unaffected (still uses `runserver` static handling) yet `DEBUG=False` env works without extra infra.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Modify `MIDDLEWARE` in `travelmathlite/core/settings.py` to insert `whitenoise.middleware.WhiteNoiseMiddleware` and set `STATICFILES_STORAGE` to manifest storage when `USE_MANIFEST_STATIC` env flag or `DEBUG` false."
- "Update `pyproject.toml` dependencies to include WhiteNoise and lock version, then regenerate `uv.lock` if applicable."
- "Write a deployment snippet documenting `uv run python manage.py collectstatic --noinput` and example WhiteNoise log output for attestation."

---
ADR: adr-1.0.7-static-media-and-asset-pipeline.md
PRD: §4 F-010; §7 NF-004
Requirements: FR-F-010-1, NF-004
