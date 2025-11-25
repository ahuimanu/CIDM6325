# BRIEF (cpb-0.1.6): Deployment Example (Docker + Gunicorn + WhiteNoise)

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §4 In Scope F-008; §7 Non-Functional (Performance/Security); §12 Rollout

ADR Anchor

- ADR-0.1.0 (Django MVP)
- ADR-0.1.1 (Bootstrap choice)
- ADR-0.1.2 (Markdown stack)

Goal

- Provide a reproducible deployment example using Docker, Gunicorn, and WhiteNoise.

Scope (single PR; ≲300 LOC not counting generated lockfiles)

- Dockerfile: Python 3.12 slim, install deps, collectstatic, run with gunicorn.
- docker-compose.yml for local dev (optional if not needed).
- Settings: add STATIC_ROOT, WhiteNoise middleware, and basic security headers for prod.
- Proc-like run: gunicorn myblog.wsgi:application --bind 0.0.0.0:8000.
- CI note (optional): add a comment or GitHub Actions stub for build/test.
- README section: how to build/run container.
- Tests: ensure app still runs; no functional code changes required.

Standards

- Keep images small; pin Python minor version; no secrets in repo; env vars for settings.

Files to touch (anticipated)

- Dockerfile (project root)
- docker-compose.yml (optional)
- blog_site/myblog/settings.py (WhiteNoise + STATIC_ROOT)
- README.MD (Deployment section)

Migration plan

- None.

Rollback

- Delete Docker-related files and WhiteNoise settings; revert commit.

Acceptance

- docker build produces an image that serves the app via gunicorn.
- Static files served by WhiteNoise; site loads main pages.
- README includes build/run instructions.

How to Test (local)

1) docker build -t cidm6325-blog .
2) docker run -p 8000:8000 cidm6325-blog
3) Visit <http://localhost:8000/blog/>

Prompts for Copilot

- Create a minimal Dockerfile with multi-stage build (optional) and gunicorn entrypoint.
- Update settings for WhiteNoise and STATIC_ROOT; don’t break DEBUG=True local setup.
- Add a short README section with commands.
