# BRIEF: Establish static/media folders and base asset wiring

Goal

- Stand up a first-class static and media folder layout so Bootstrap, site branding, and optional avatars load from local assets instead of public CDNs (PRD §4 F-007/F-010; §7 NF-004). This unlocks hashed filenames and WhiteNoise in later briefs.

Scope (single PR)

- Files to touch: `travelmathlite/core/settings.py`, `travelmathlite/templates/base.html`, new `travelmathlite/static/` (vendor + site bundles), placeholder `travelmathlite/media/.gitkeep` (ignored in git but path documented).
- Tasks: define `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT`; add `django.contrib.staticfiles` template context support where missing; move Bootstrap CSS/JS + favicons into `travelmathlite/static/vendor/` and update templates to `{% load static %}` and reference local assets.
- Non-goals: WhiteNoise middleware, Manifest storage toggles, avatar upload forms (handled in later briefs).

Standards

- Commits: conventional (`feat/docs/refactor`) and reference issues with `Refs #N` / `Closes #N`.
- Use `uv run python manage.py collectstatic --dry-run` locally to validate settings; lint/format with Ruff.
- Django tests: `TestCase` only (no pytest); prefer fixture-free tests.

Acceptance

- Base template and shared partials load Bootstrap assets via `{% static %}` and no longer hit external CDNs.
- `collectstatic --dry-run` reports vendor files under `STATICFILES_DIRS`, and `STATIC_ROOT`/`MEDIA_ROOT` resolve under `<repo>/travelmathlite/staticfiles/` and `<repo>/travelmathlite/media/` (path names configurable via env vars but default documented).
- Documented folder tree snippet added to `docs/travelmathlite/ops/static-and-media.md` covering where to drop branding assets for designers.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Update `travelmathlite/core/settings.py` with `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT`, and helper env overrides for production builds."
- "Refactor `travelmathlite/templates/base.html` to `{% load static %}` and use local Bootstrap CSS/JS from `static/vendor/bootstrap/` with integrity metadata removed."
- "Produce a short docs snippet explaining how to add brand images under `travelmathlite/static/img/` and where collectstatic writes output."

---
ADR: adr-1.0.7-static-media-and-asset-pipeline.md
PRD: §4 F-007, F-010; §7 NF-004
Requirements: FR-F-007-1, FR-F-010-1, NF-004
