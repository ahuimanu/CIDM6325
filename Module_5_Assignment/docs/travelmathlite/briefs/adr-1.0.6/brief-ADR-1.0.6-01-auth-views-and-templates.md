# BRIEF: Wire Django auth views and templates

Goal

- Enable login/logout/register using Django’s built-in auth views, themed with our base templates. Ensure routes, templates, and redirects align with TravelMathLite UX and seed the path for saving calculations to user accounts (PRD §4 F-006; §7 NF-003).

Scope (single PR)

- Files to touch: `apps/accounts/urls.py`, `apps/accounts/templates/registration/*.html` (login, logout, signup, password reset), base nav/login links in `templates/base.html`.
- Behavior: Wire `django.contrib.auth` views; add signup view using `UserCreationForm`; set `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` as needed; ensure CSRF and messages framework hooks are present.
- Non-goals: Social auth; email verification flows; saved calculations UI.

Standards

- Commits: conventional (feat/docs); include Issue reference with Refs/Closes.
- Use `uv run` for Django tasks; lint/format with Ruff.
- Django tests: `TestCase` only (no pytest).

Acceptance

- Auth pages render and function: login, logout, signup; redirects correct.
- Templates extend site base and include CSRF and messages.
- Anonymous users see login/register nav; authenticated users see profile/logout.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add auth URL patterns under `apps/accounts/urls.py` delegating to Django auth views; include login, logout, password reset; add a simple `SignupView` based on `UserCreationForm`."
- "Create `apps/accounts/templates/registration/login.html` and `.../signup.html` extending `base.html` with CSRF, username/password fields, and error display."
- "Update `templates/base.html` nav to show Login/Signup or Username/Logout depending on `request.user.is_authenticated`."

---
ADR: adr-1.0.6-auth-and-saved-calculations-model.md
PRD: §4 F-006; §7 NF-003
Requirements: FR-F-006-1, NF-003
