```markdown
# BRIEF ADR-1.0.8-03: Production security hardening & WhiteNoise

Goal

- Implement prod settings that enable security middleware, secure cookies, CSRF hardening, security headers, and WhiteNoise static serving as described in ADR-1.0.8.

Scope (single PR)

- Files to touch: `project/settings/prod.py`, `requirements.txt` (add `whitenoise` if not present), `docs/ops/settings.md` (update), and minimal tests.
- Non-goals: full deployment automation (e.g., Gunicorn, systemd) or HTTPS certificate provisioning.

Standards

- Follow Django security checklist recommendations: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`.
- Use WhiteNoise for static files in prod and document when it's appropriate to remove it for CDN usage.

Acceptance

- `prod.py` enables security middleware and sets the secure cookie flags; `DEBUG=False` by default.
- WhiteNoise integrated and a short note on when to use it vs CDN.
- `requirements.txt` updated if WhiteNoise added.

Prompts for Copilot

- "Add recommended production security settings to `prod.py` with env-controlled values and comments explaining tradeoffs."
- "Add WhiteNoise configuration snippet and requirements file change."

Notes

- Ensure tests assert that required security flags exist when importing `prod.py`.

```
