Authentication & Authorization — Implementation Notes

This project implements user registration, login, logout, and role-based permissions. This document describes what is implemented, how to use it, and security/usability considerations.

Implemented features

- Registration
  - Endpoint: `POST /accounts/register/` (view: `blog.views.register`)
  - Uses Django's `UserCreationForm`. After successful registration the new user is logged in and redirected to the post list.

- Login / Logout
  - Custom login view: `POST /accounts/login/` (view: `blog.views.login_view`) — this view provides case-insensitive username matching and email fallback for convenience.
  - Logout and other auth views: included via `django.contrib.auth.urls` (project-level `blogsite/urls.py`).

- Dev helper login
  - `GET /dev-login/` (view: `blog.views.dev_login`) — creates and logs in a development superuser `dev` / `devpass` when `DEBUG=True` (useful for local testing). Guarded by DEBUG check and localhost checks.

- Role-based permissions
  - The `Post` model declares custom permissions: `can_review` and `can_publish` in `Post.Meta.permissions`.
  - Views enforce permissions in several places:
    - `review_list` requires `blog.can_review` to access the review queue.
    - Publishing actions are gated by `blog.can_publish` (both in FBV and CBV versions).
    - Editing is allowed for the author or users with `blog.change_post`.
    - Deletion is gated by `blog.delete_post`.

How to set up roles (quick)

- Option 1: Admin UI
  - Create a superuser and visit `/admin/`.
  - Create groups (e.g., `editor`, `publisher`) and assign the appropriate permissions from the `Post` model.

- Option 2: Management command (provided)
  - A management command `create_roles` is included to create three groups and assign permissions automatically:

```powershell
.venv\Scripts\python.exe manage.py create_roles
```

  - This command creates/updates groups named `editor`, `publisher`, and `maintainer` and assigns permissions such as `change_post`, `can_review`, and `can_publish`.

Security considerations

- Passwords and secret management
  - Use a strong SECRET_KEY in production and do not keep `DEBUG=True` in production.
  - The project includes `python-dotenv` in `requirements.txt` — use environment variables (or `.env`) to store secrets.

- Dev helpers
  - `dev_login` is convenient for local development but must never be enabled in production. It is guarded by `settings.DEBUG` and remote IP checks, but verify it is removed or disabled in any deployed environment.

- Permissions and least privilege
  - Use groups to assign minimal necessary permissions. Editors should get `can_review` and `change_post` if they need to edit; publishers get `can_publish`.
  - Avoid making too many users superusers; prefer group-based permissions.

- CSRF & session security
  - Django's CSRF middleware is enabled by default and should remain enabled.
  - Consider setting `SESSION_COOKIE_SECURE=True` and `CSRF_COOKIE_SECURE=True` in production (HTTPS required) and `SESSION_COOKIE_AGE` to reasonable expiry.

Usability considerations

- Login convenience
  - The custom `login_view` supports case-insensitive username matching and allows users to log in with email (if present). This improves UX but should be documented for support.

- Registration friction
  - The current registration flow logs users in immediately after creation. This reduces friction but consider email verification for production to prevent spam accounts.

- Permission discovery
  - Admins may need a one-page guide (or the provided `create_roles` command) listing which permissions to assign for common roles. The `ADMIN_USAGE.md` file documents common admin workflows.

Verification steps

1. Run migrations and create roles (optional):

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py create_roles
```

2. Create a superuser:

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

3. Start the server and exercise flows:

```powershell
.venv\Scripts\python.exe manage.py runserver
# Visit http://127.0.0.1:8000/accounts/register/ to register
# Visit http://127.0.0.1:8000/accounts/login/ to login
# Visit http://127.0.0.1:8000/dev-login/ (if DEBUG=True) to quickly get an admin
# Visit /posts/new/ to create a post; publishing requires can_publish permission
# Visit /posts/review/ to see review queue (requires can_review)
```

If you want, I can add automated tests that assert the permission checks (e.g., reviewer can't publish) or wire the `create_roles` command into your test setup. Let me know which you'd prefer.
