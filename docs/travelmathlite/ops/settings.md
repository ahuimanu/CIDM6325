## Settings and environment variables (ops)

This document describes required and recommended environment variables for running TravelMathLite and how reviewers/operators should validate settings in local and production modes.

Location

- Example env file: `travelmathlite/.env.example`
- Copy to `travelmathlite/.env` for local development (the project reads this via `django-environ` in `core.settings`).

Required / Recommended environment variables

- `SECRET_KEY` (required in production): Django secret key. Never commit a real secret to git.
- `DJANGO_DEBUG` (optional): `1` or `0`. Local default is `1`.
- `DATABASE_URL` (recommended): Database connection URL. Default local: `sqlite:///db.sqlite3`.
- `ALLOWED_HOSTS` (required in production): Comma-separated list of allowed hosts.
- `EMAIL_URL` (optional): Email delivery URL for transactional email in prod.
- `USE_WHITENOISE` (optional): `1` to enable WhiteNoise static serving in WSGI wrapper.
- `USE_MANIFEST_STATIC` (optional): `1` to enable manifest staticfiles storage for hashed assets.
- `STATIC_ROOT` / `MEDIA_ROOT` (optional): override default paths for static and media dumps.
- `SENTRY_DSN` (optional): Error reporting DSN.

Local development quickstart

1. Copy the example env file into the project:

```bash
cp travelmathlite/.env.example travelmathlite/.env
```

2. (Optional) Edit `travelmathlite/.env` to change `DJANGO_DEBUG=1` or other local defaults.

3. Run migrations and start the server (from repo root):

```bash
uv run python travelmathlite/manage.py migrate
uv run python travelmathlite/manage.py runserver
```

Notes: `core.settings` defaults to local development settings (`core.settings` re-exports `core.settings.local`). To explicitly use production settings locally for testing, set `DJANGO_SETTINGS_MODULE=core.settings.prod`.

How to test production settings locally (smoke checks)

Run this from the `travelmathlite/` directory or set `PYTHONPATH` appropriately. The example below runs with the `prod` settings import and prints key flags:

```bash
# Example: run in project root
DJANGO_SETTINGS_MODULE=core.settings.prod \
  python - <<'PY'
import importlib
try:
    prod = importlib.import_module('core.settings.prod')
    print('DEBUG=', getattr(prod, 'DEBUG', None))
    print('ALLOWED_HOSTS=', getattr(prod, 'ALLOWED_HOSTS', None))
except Exception as e:
    print('Error importing prod settings:', e)
    raise
PY
```

Or use the built-in management command which prints a concise summary of key settings:

```bash
# Run with the same settings module you want to inspect
DJANGO_SETTINGS_MODULE=core.settings.prod uv run python travelmathlite/manage.py check_settings
```

Expected output includes lines similar to:

```
Settings quick-check:
DJANGO_SETTINGS_MODULE: core.settings.prod
DEBUG: False
ALLOWED_HOSTS: ['example.com']
SECRET_KEY present: True
SESSION_COOKIE_SECURE: True
CSRF_COOKIE_SECURE: True
USE_WHITENOISE: True
```

Reviewer checklist (pre-merge / ops review)

- [ ] `SECRET_KEY` is not in the repository and is provided via environment in prod.
- [ ] `ALLOWED_HOSTS` is configured for the deployment domain(s).
- [ ] `DEBUG` is `False` in production config.
- [ ] Security flags set: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT` (as appropriate).
- [ ] Static assets: `collectstatic` runs and `STATIC_ROOT` is writable; for hashed assets `USE_MANIFEST_STATIC=1`.

Troubleshooting

- If `core.settings.prod` import fails with `ImproperlyConfigured`, ensure `SECRET_KEY` and `ALLOWED_HOSTS` are set in the environment (or the `.env` used for test).
- For static file issues, run `uv run python travelmathlite/manage.py collectstatic --noinput --clear` and inspect `STATIC_ROOT`.

References

- ADR: `docs/travelmathlite/adr/adr-1.0.8-settings-configuration-and-secrets.md`
- Briefs: `docs/travelmathlite/briefs/adr-1.0.8/`
