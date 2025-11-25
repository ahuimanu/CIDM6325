# BRIEF: Static/media tests and visual attestation

Goal

- Add automated coverage plus a Playwright visual check proving hashed assets and media links work across the base layout and avatar upload acceptance criteria (PRD §4 F-007/F-010; §7 NF-004).

Scope (single PR)

- Files to touch: `apps/base/tests/`, `apps/accounts/tests/`, `travelmathlite/scripts/visual_checks/` (or existing Playwright script), `docs/travelmathlite/screenshots/` for evidence, CI configuration referencing the new script.
- Tasks: write Django tests ensuring `static('css/site.css')` renders hashed URLs when `USE_MANIFEST_STATIC=1`; add avatar upload integration test verifying media URL; extend Playwright script to load `/` with `DEBUG=False` env and capture network panel screenshot or CLI log of hashed assets; document how to store the screenshot + transcript.
- Non-goals: Browserstack runs, CDN smoke tests, performance benchmarking.

Standards

- Commits: `test/chore/docs` with Issue refs.
- Tests must run via `uv run python manage.py test` and clean up media files via `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')` where needed.
- Playwright artifacts stored under `travelmathlite/screenshots/static-pipeline/` with timestamped filenames.

Acceptance

- Unit tests cover invariants `INV-1` (static URLs resolve) and `INV-2` (manifest rewrites) with assertions referencing hashed file names.
- Playwright script runs headless, loads `/` and `/accounts/profile/`, ensures CSS/JS responses come from `/static/` (not CDN), and exports screenshot/log to docs for attestation.
- README (or ops doc) links to screenshot folder and describes how to re-run the script.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create a Django test case that toggles `USE_MANIFEST_STATIC` and uses `self.client.get('/')` to assert `bootstrap.min.css` link includes a hashed suffix."
- "Extend the Playwright script under `travelmathlite/scripts/` to wait for `link[rel=stylesheet][href*='/static/']` responses and capture screenshots into `screenshots/static-pipeline/`."
- "Document the attestation workflow in `docs/travelmathlite/ops/static-and-media.md`, including where to store screenshots and how to attach them to ADR evidence."

---
ADR: adr-1.0.7-static-media-and-asset-pipeline.md
PRD: §4 F-007, F-010; §7 NF-004
Requirements: FR-F-007-1, FR-F-010-1, NF-004
