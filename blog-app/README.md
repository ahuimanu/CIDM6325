# CIDM6325 — Django Blog (Module 3)

Summary

This repository implements a Django blog for the Module 3 assignment. The project implements authentication, CRUD, editorial workflow, custom forms and validation, HTMX interactions, basic accessibility improvements, tests, and CI.

Quick start (PowerShell)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ after starting the server.

Assignment mapping (what to grade)

Part A — Forms & Validation (30 pts)
- Implemented: `blog/forms.py` (`PostForm`, `CommentForm`) with `clean_title`, `clean`, banned-word checks, and `save(author=...)` that parses `tags_csv`. See tests in `blog/tests.py` for coverage.

Part B — Multi-Model Design (30 pts)
- Implemented: `blog/models.py` defines `Post`, `Tag` (ManyToMany), and `Comment` (FK). See `SCHEMA.md` for Mermaid ER diagram and migration notes.

Build a Blog Feature Set — Auth/CRUD/Workflow (40 pts)
- Implemented: authentication (register/login/logout), post create/edit/delete, editorial workflow (`draft` → `review` → `published`), and role-based permissions (`can_review`, `can_publish`). Key files: `blog/views.py`, `blog/urls.py`, `templates/`.

Part C — Reflection on AI-assisted Modeling (15 pts)
- Implemented: `REFLECTION.md` contains a ~500-word reflection describing how AI supported model/form design, including prompt examples and critiques.

### Part D. Peer Review (15 points)
tdb


### Part E. DjangoVMS Journey Critique (10 points)
tbd


HTMX and Accessibility
- HTMX: live search and inline edit endpoints implemented (`hx_post_search`, `hx_post_inline_edit`) and covered by tests in `blog/tests.py`.
- Accessibility: `ACCESSIBILITY.md` documents checks and improvements; the login template was updated to expose error containers and help text ids. Additional per-field ARIA and contrast checks are recommended as follow-ups.

CI and Tests
- `.github/workflows/ci.yml` runs migrations and the test suite on push/PR.
- Test suite: `blog/tests.py` includes form, auth, permissions, workflow, and HTMX tests. Tests run successfully in the provided virtual environment.

Files of interest (quick reference)
- `blog/models.py` — Post, Tag, Comment (schema)
- `blog/forms.py` — PostForm, CommentForm (validation)
- `blog/views.py` — CRUD, HTMX endpoints, auth helpers
- `blog/tests.py` — unit tests (forms, auth, review workflow, HTMX)
- `SCHEMA.md` — Mermaid ER diagram, migration notes, business/analytics assumptions
- `ACCESSIBILITY.md` — accessibility checklist and implementation notes
- `REFLECTION.md` — reflection on AI-assisted modeling
- `.github/workflows/ci.yml` — CI workflow

Grader quick verification steps
1. Create a virtual env and install dependencies.
2. Run `python manage.py migrate` and `python manage.py test` — tests should pass.
3. Start the server and exercise the app: register, create a post, move to review, and publish with an account that has `can_publish`.

Optional extras I can add on request
- Rendered SVG of the Mermaid diagram (for viewers without Mermaid support).
- Per-field ARIA error IDs across forms (accessibility hardening).
- A one-page grading checklist for submission.

