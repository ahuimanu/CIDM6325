# CIDM 6325 — Weeks 5–6: Blog with Forms, Validation, and Multi-Model Design

This repo contains a minimal Django app aligned to the assignment rubric.

## Feature Checklist (rubric mapping)
- [x] Auth: login/logout via `django.contrib.auth`
- [x] CRUD for **Post** (create/update/delete guarded by author)
- [x] Multi-model: `Category`, `Tag`, `Post`, `Comment` (O2M + M2M)
- [x] Role-based permission: `blog.can_publish` (publish action)
- [x] Forms: `PostForm` & `CommentForm` with `clean()` validation
- [x] HTMX: live search on post list (`/search/`)
- [x] Bootstrap UI & accessibility notes (WCAG 2.2)
- [x] CI/CD demo: GitHub Actions workflow
- [x] Public repo & documentation stubs

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Accessibility (WCAG 2.2) Notes
- Form controls have `<label>` associations and helpful text.
- Visible focus styles; color-contrast via Bootstrap defaults; no color-only cues.
- Live regions: messages area uses `role="status"` semantics via alerts.
- Keyboard-friendly: links and buttons in tab order; ARIA labels on search.

## HTMX Interactions
- Type in the search field on `/` to fetch filtered results from `/search/` and update `#list`.
- Extend with inline editing by posting to your update endpoints and returning a row partial.

## Role-Based Permissions
- Add `can_publish` to a group (e.g., Editors). Users in that group can hit `/post/<pk>/publish/`.
  ```bash
  # in Django admin -> Auth -> Groups -> add permission "blog | post | Can publish posts"
  ```

## Schema & Migrations
- Relationships:
  - `Category (1) -- (M) Post`
  - `Post (M) -- (M) Tag`
  - `Post (1) -- (M) Comment`
- Generate diagram (optional):
  ```bash
  pip install django-extensions pydot
  python manage.py graph_models blog -o schema.png
  ```

## Deployment Notes
- Includes Whitenoise for static files. For production, set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- You can deploy on Render, Railway, or GitHub Codespaces.

---

See `AI_Reflection_Week5_6.md` and `PRD_Update.md` for write-ups.
