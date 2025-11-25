# Static and Media (Ops)

This document explains the layout and operator steps for static assets and media in TravelMathLite.

Folder layout (defaults)

- `travelmathlite/static/` — place design and vendor source files (CSS, JS, images). Example: `travelmathlite/static/vendor/bootstrap/` and `travelmathlite/static/img/`.
- `travelmathlite/staticfiles/` — default `STATIC_ROOT` target where `collectstatic` places compiled/collected assets for deployment. This path can be overridden with `STATIC_ROOT` env var.
- `travelmathlite/media/` — `MEDIA_ROOT` for user-uploaded content (avatars, uploaded images). This path can be overridden with `MEDIA_ROOT` env var.

Developer workflow (local)

1. Add vendor or site assets under `travelmathlite/static/` in the appropriate subfolders. For example, put `bootstrap.min.css` at `static/vendor/bootstrap/css/bootstrap.min.css`.
2. In templates, reference assets using the `static` template tag: `{% load static %}` and `<link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">`.
3. To verify settings without writing files, run a dry-run:

```bash
# from repo root in bash
uv run python manage.py collectstatic --dry-run
```

Operator/deploy workflow

- Before deploying to a demo/prod environment, ensure `collectstatic` has run and artifacts are present under `STATIC_ROOT`.

Example deploy checklist snippet (preferred):

```bash
# Preferred: use the project helper which emits logs and a concise summary
# Run from repo root (bash example):
uv run python scripts/run_collectstatic.py --noinput --log-dir docs/travelmathlite/ops/logs --archive-logs
```

If you prefer to call `manage.py` directly, the old pattern continues to work:

```bash
# Optional: export env overrides
export STATIC_ROOT=/opt/app/staticfiles
export MEDIA_ROOT=/opt/app/media
export USE_MANIFEST_STATIC=1  # enable only when also configuring WhiteNoise/Manifest

# Run collectstatic and capture transcript for attestation
uv run python manage.py collectstatic --noinput | tee collectstatic-$(date +%Y%m%d-%H%M%S).log
```

Notes & guidance

- For course/demo deployments we use WhiteNoise + `ManifestStaticFilesStorage` in later ADRs. For now, ensure local templates do not point to external CDNs if you want fully offline demos; store vendor files under `static/vendor/`.
- Keep vendor assets small. If replacing with upstream distribution, prefer the minified bundles.
- `media/` is in `.gitignore`; do not commit uploaded user files. Use `media/.gitkeep` to ensure the folder is present on disk if needed.

Troubleshooting

- If `collectstatic` reports missing files referenced in templates, double-check the `{% static %}` path and that files exist under `travelmathlite/static/` or another `STATICFILES_DIRS` path.
- If templates still load CDN assets, ensure you've removed the CDN links and replaced them with `{% static %}` references, then run `collectstatic`.

Evidence and attestation

- Save the `collectstatic` log and any screenshots of the site showing local assets under `docs/travelmathlite/screenshots/` for ADR evidence.
- When using `scripts/run_collectstatic.py`, a timestamped log and a concise `collectstatic-summary-*.md` are produced under `docs/travelmathlite/ops/logs/` and may be attached to the ADR evidence folder. The `--archive-logs` flag produces a `.tar.gz` of the raw log files for archival.

CI Example (GitHub Actions)

```yaml
name: collectstatic-and-evidence
on: [workflow_dispatch]
jobs:
  collectstatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run collectstatic (prod-like)
        env:
          DJANGO_SETTINGS_MODULE: travelmathlite.core.settings
          DEBUG: 'False'
          USE_MANIFEST_STATIC: '1'
        run: |
          uv run python scripts/run_collectstatic.py --noinput --log-dir docs/travelmathlite/ops/logs --archive-logs
      - name: Upload logs
        uses: actions/upload-artifact@v4
        with:
          name: collectstatic-evidence
          path: docs/travelmathlite/ops/logs/
```

How to run the static/media tests and visual attestation

- Run Django unit tests (the new tests validate static URL behavior):

```bash
# from repo root
uv run python manage.py test apps.base.tests.test_static_pipeline
```

- Run the visual check (Playwright) after starting the site locally:

```bash
# Ensure Playwright is installed and browsers are available
pip install playwright
playwright install

# Start the dev server in another terminal (repo root):
uv run python manage.py runserver

# Run the visual check (writes PNG + links file under travelmathlite/screenshots/static-pipeline/)
uv run python travelmathlite/scripts/visual_checks/static_pipeline_check.py --url http://127.0.0.1:8000
```

Attach the resulting screenshot and links file to the ADR evidence folder when closing the brief.
