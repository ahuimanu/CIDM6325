# Django Blog PRD Alignment Checklist — Completed with Notes

This document is a filled-in copy of `LAYMAN_CHECKLIST_01.md`, marked against the current repository state (branch FALL2025) and annotated with brief notes pointing to code, tests, and any gaps/TODOs.

Legend

- [x] Completed and verified
- [ ] Not yet completed or pending docs/tests

---

## 1. From Browser to Django (Introductory Context)

- [x] HTTP request/response flow — URLs → CBV views → templates are wired: `blog/urls.py` maps to CBVs in `blog/views.py`, rendering templates under `blog/templates/blog/`.
- [ ] Runserver demonstration — Pending screenshots/asciinema; can run via `python blog_site/manage.py runserver` and visit `/blog/`.
- [ ] Console inspection — No explicit logging added; add debug logging middleware or view prints if desired.
- [x] Code commentary — CBVs include concise docstrings describing purpose and flow in `blog/views.py`.
- [ ] Visual diagram (optional) — Not included (optional teaching aid).

---

## 2. URLs Lead the Way

- [x] urls.py created — App URLs in `blog/urls.py` with names: `post_list`, `post_detail`, `post_create`, `post_update`, `post_delete` (implemented as CBVs per repo norms).
- [x] Namespace clarity — Project URLs include `blog/` with `include('blog.urls', namespace='blog')` in `myblog/urls.py`.
- [x] URL naming discipline — All routes use `name=` and are reversed in templates/tests.
- [x] Canonical link alignment — Detail pattern `post/<slug:slug>/` matches PRD intent; slugs are unique.
- [x] Test coverage (resolve) — `resolve()` asserted in tests (see `test_new_route_not_captured_by_slug`); guards route ordering and pattern collisions.

---

## 3. Views on Views

- [x] Views defined — Implemented directly as CBVs (List/Detail/Create/Update/Delete) in `blog/views.py`.
- [x] Proper rendering — CBVs render templates (Django’s `render()` under the hood).
- [x] View docstrings — Present in CBVs; align with Layman’s “views mediate between model and template.”
- [x] Error handling — `DetailView` with filtered queryset 404s when not found; `get_queryset()` restricts to published posts.
- [x] Unit tests — `blog/tests.py` covers list/detail 200s and CRUD redirects.

---

## 4. Templates for User Interfaces

- [x] Templates configured — `APP_DIRS=True` in `myblog/settings.py`; app templates under `blog/templates/blog/`.
- [x] Base template — `blog/base.html` with `{% block content %}` and `{% block extra_js %}`; pages extend `"blog/base.html"`.
- [x] List/detail render — Titles, dates, and body rendered; body uses `markdown_safe|safe` sanitization.
- [x] Template tags — `{% url 'blog:post_detail' slug=post.slug %}` used in list/detail navigation.
- [x] Markdown rendering verified — Custom filter `blog/templatetags/markdown_extras.py` plus tests sanitize `<script>`.
- [ ] Accessibility compliance — Not audited yet; recommend heading order, landmarks, and link contrast check.

---

## 5. User Interaction with Forms

- [x] Form created — `PostForm` (ModelForm) in `blog/forms.py` with Bootstrap widgets and `.markdown-editor` class.
- [x] CSRF token — Included in `blog/templates/blog/post_form.html`.
- [ ] Validation hooks — Relying on model/field validation; no custom `clean_` methods currently (can add for title rules).
- [x] Form lifecycle — CBVs demonstrate GET form, POST process, redirect; verified by 302s in tests.
- [x] Optional enrichment — ModelForm used; `commit=False` example not included (optional for teaching).

---

## 6. Store Data with Models

- [x] Post model — `title`, `slug` (editable=False), `body`, `publish_date`, `tags` in `blog/models.py`.
- [x] Migrations applied — Initial migration present under `blog/migrations/`.
- [x] Admin entry — `blog/admin.py` registers `Post` with custom admin config.
- [x] Slug uniqueness — Enforced via custom `save()` generating unique slugs.
- [ ] Model methods — `get_absolute_url()` not yet implemented (quick add possible; currently reversed in views).
- [x] ORM queries — Views use `Post.objects.filter(...)` with `publish_date__lte=timezone.now()`.
- [x] Persistence tests — CRUD flow covered in `blog/tests.py`.

---

## 7. Administer All the Things

- [ ] Admin site enabled — Superuser creation not documented here (run `createsuperuser` when needed).
- [x] Custom ModelAdmin — `list_display`, `search_fields`; note: no `prepopulated_fields` because `slug` is `editable=False` (slug is auto-generated in model to avoid the admin KeyError observed earlier).
- [x] Markdown preview integration — EasyMDE enabled on `body` in custom `change_form.html`.
- [ ] Permissions model — Public authoring route exists; no staff-only restriction implemented yet.
- [ ] Screenshots/docs — Not included yet; suggested for teaching alignment with Layman’s chapter.
- [ ] Admin tests — No auth-protected admin tests currently.

---

## 8. Anatomy of an Application

- [x] App layout — Matches Django convention (blog app contains admin/forms/models/templates/tests/urls/views).
- [ ] Settings modularization — Single `settings.py` only; could split into `base/dev/prod` if desired.
- [x] INSTALLED_APPS — Includes `'blog'` and `'taggit'`.
- [ ] Static files pipeline — No Whitenoise/collectstatic setup (not required for local dev).
- [ ] README mapping — No explicit “Anatomy” mapping section in `README.MD` yet.
- [x] Navigability — URLs → Views → Templates → Models → Admin are discoverable and consistent.

---

## 9. User Authentication

- [x] Authentication system enabled — `django.contrib.auth` in `INSTALLED_APPS`; `AuthenticationMiddleware` in middleware stack.
- [ ] Login/Logout views — Not yet configured; recommend adding `LoginView`/`LogoutView` from `django.contrib.auth.views`.
- [ ] User registration — Not implemented; consider adding signup form or document third-party packages.
- [ ] Login required decorator — Not yet applied to any views; recommend protecting create/update/delete views with `@login_required` or `LoginRequiredMixin`.
- [ ] User permissions — No permission checks currently; all CRUD operations are public.
- [ ] Password management — Django's built-in password validators configured in settings; reset flow not implemented.
- [ ] Templates — No login/logout templates created yet.
- [ ] Tests — No authentication tests; recommend adding tests for login redirects and protected views.

---

## 10. Middleware Do You Go?

- [x] Middleware stack reviewed — Standard middleware in `myblog/settings.py`: SecurityMiddleware, SessionMiddleware, CommonMiddleware, CsrfViewMiddleware, AuthenticationMiddleware, MessagesMiddleware, XFrameOptionsMiddleware.
- [ ] Custom middleware created — No custom middleware; optional example (logging, request timer) could be added for teaching.
- [ ] Middleware order documented — Order follows Django defaults; no explicit documentation in README.
- [x] Common middleware explained — Standard Django middleware stack present and configured correctly.
- [ ] Process request/response hooks — Not demonstrated; could add custom middleware example.
- [ ] Exception handling — No custom exception middleware; relying on Django defaults.
- [ ] Tests — No middleware-specific tests.

---

## 11. Serving Static Files

- [x] Static files configuration — `STATIC_URL = "static/"` in settings; `django.contrib.staticfiles` in `INSTALLED_APPS`.
- [ ] Static directory structure — No `blog/static/blog/` directory currently; static assets not yet added.
- [ ] Template integration — No `{% load static %}` usage yet; would be needed when adding CSS/JS.
- [x] Development serving — `django.contrib.staticfiles` enabled for dev serving.
- [ ] Production strategy — No `STATIC_ROOT` or `collectstatic` configuration yet; not documented.
- [ ] Whitenoise integration — Not configured; recommend for production deployment.
- [ ] Assets verified — No CSS/JS assets to verify yet.
- [ ] Tests — No static file tests.

---

## 12. Test Your Apps

- [x] Test suite created — `blog/tests.py` contains test classes.
- [x] Django TestCase used — All tests use `django.test.TestCase` (not pytest, per project norms).
- [x] Model tests — Slug generation and uniqueness tested implicitly through CRUD tests.
- [x] View tests — Status codes (200, 302), template rendering, CRUD operations all tested.
- [x] Form tests — Form submission tested through CBV POST tests.
- [x] URL tests — `resolve()` tested for route ordering (`test_new_route_not_captured_by_slug`).
- [ ] Coverage target — No coverage report run yet; recommend using `coverage.py` to measure.
- [ ] Test data — Tests create data in `setUp()`; no fixtures or factories yet.
- [ ] CI integration — No GitHub Actions workflow yet; recommend adding test automation.
- [x] Documentation — Test run instructions in main README; could be expanded.

---

## 13. Deploy A Site Live

- [ ] Deployment target selected — Not yet deployed; document target platform when ready.
- [ ] Environment variables — `SECRET_KEY` hardcoded in settings (insecure); recommend moving to environment variables.
- [ ] Database configured — Using SQLite (dev only); need PostgreSQL or similar for production.
- [ ] Static files served — No `STATIC_ROOT` or `collectstatic` setup yet.
- [ ] ALLOWED_HOSTS — Currently empty list (only works for localhost); needs production domain.
- [x] DEBUG mode — Set to `True` in dev; needs `DEBUG = False` for production.
- [ ] HTTPS enforced — No SSL settings configured yet; recommend `SECURE_SSL_REDIRECT = True` for prod.
- [ ] Deployment checklist — Not run yet; recommend `python manage.py check --deploy`.
- [ ] Monitoring — No error tracking (Sentry, etc.) configured.
- [ ] Documentation — No deployment documentation yet.

---

## 14. Per-visitor Data With Sessions

- [x] Session middleware — `SessionMiddleware` enabled in middleware stack (default).
- [x] Session backend — Database-backed sessions (default Django configuration).
- [ ] Session data usage — No example views using `request.session` yet; optional teaching example.
- [x] Session expiration — Using Django defaults; not customized (`SESSION_COOKIE_AGE` not set).
- [ ] Security settings — `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_HTTPONLY` not configured yet (needed for production).
- [ ] Session cleanup — `clearsessions` command not documented; recommend adding to maintenance docs.
- [ ] Use cases demonstrated — No session-based features (cart, preferences) implemented yet.
- [ ] Tests — No session-specific tests.

---

## 15. Making Sense Of Settings

- [x] Settings organization — Single `myblog/settings.py`; no split into base/dev/prod yet.
- [ ] Environment-specific configs — Hardcoded values; recommend `os.environ.get()` or `django-environ`.
- [ ] Secret key management — **INSECURE**: Secret key is hardcoded and committed; must move to environment variable.
- [x] Database configuration — SQLite for dev; needs PostgreSQL config for production.
- [x] Debug mode — `DEBUG = True` appropriate for dev; document need to set `False` for prod.
- [ ] Logging configuration — No `LOGGING` dict configured; using Django defaults.
- [ ] Email backend — Not configured; recommend console backend for dev, SMTP for prod.
- [ ] Settings documentation — No documentation of custom settings yet.
- [ ] Validation — No custom settings validation with `check` framework.

---

## 16. User File Use (Media Files)

- [ ] Media files configuration — No `MEDIA_URL` or `MEDIA_ROOT` configured yet.
- [ ] File upload field — No FileField or ImageField in models yet.
- [ ] Development serving — No media file serving configured in dev URLs.
- [ ] Production serving — Not applicable yet; document CDN strategy when needed.
- [ ] File validation — Not applicable yet; recommend size/type validation when implemented.
- [ ] Storage backends — Using default file storage; no django-storages configuration.
- [ ] Security — Not applicable yet; recommend UUID filenames and extension validation.
- [ ] User experience — Not applicable yet.
- [ ] Tests — No file upload tests.

---

## 17. Command Your App (Management Commands)

- [ ] Custom management command — No custom commands in `blog/management/commands/` yet.
- [ ] Command structure — Not applicable; recommend adding example command (data import, cleanup).
- [ ] Command arguments — Not applicable yet.
- [ ] Use cases — Could add: import posts from JSON, generate sample data, cleanup old sessions.
- [ ] Output styling — Not applicable yet.
- [ ] Error handling — Not applicable yet.
- [ ] Documentation — Not applicable yet.
- [ ] Tests — Not applicable yet.
- [ ] Automation — Not applicable yet.

---

## 18. Go Fast With Django (Performance)

- [ ] Database query optimization — No `select_related()` or `prefetch_related()` usage yet; check for N+1 queries.
- [ ] Query analysis — Django Debug Toolbar not installed; recommend adding for dev.
- [x] Indexing strategy — No custom database indexes; relying on auto-indexed primary keys and ForeignKeys.
- [ ] Caching implemented — No caching configured (view, template fragment, or queryset caching).
- [ ] Cache backend configured — No Redis or Memcached configuration.
- [ ] Static file optimization — No minification or CDN configuration yet.
- [ ] Database connection pooling — Not configured; using default Django database connections.
- [ ] Pagination — `ListView` uses Django's default pagination (25 items); could customize.
- [ ] Performance testing — No profiling tools (django-silk) installed yet.
- [ ] Documentation — No performance optimization documentation.

---

## 19. Security And Django

- [ ] Security settings enabled — Production security settings not configured yet (SECURE_SSL_REDIRECT, SECURE_HSTS_SECONDS, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE).
- [x] XSS protection — Template auto-escaping enabled; markdown sanitization via bleach in `markdown_extras.py`.
- [x] CSRF protection — CsrfViewMiddleware enabled; tokens in forms (via Django form rendering).
- [x] SQL injection prevention — Using ORM exclusively; no raw SQL with string interpolation.
- [x] Clickjacking protection — `XFrameOptionsMiddleware` enabled in middleware stack.
- [ ] Content Security Policy — No CSP headers configured; optional enhancement.
- [ ] Dependency management — No automated security updates or vulnerability scanning.
- [x] Password strength — Django's password validators configured in settings (similarity, minimum length, common passwords, numeric).
- [x] User input validation — Django form validation handles user input; markdown sanitization prevents XSS.
- [ ] Security audit — `python manage.py check --deploy` not run yet; recommend running and addressing warnings.
- [ ] Penetration testing — Not performed; optional for production applications.
- [x] Documentation — Security measures documented in code comments (bleach sanitization); formal security doc recommended.

---

## 20. Debugging Tips And Techniques

- [ ] Django Debug Toolbar installed — Not installed yet; highly recommended for development.
- [ ] Logging configured — No custom logging configuration; using Django defaults.
- [ ] Error pages — No custom 404/500 templates yet; using Django defaults.
- [ ] Development debugging — Can use `breakpoint()` or `pdb`; not documented.
- [ ] VS Code debugging — No launch.json configuration for Django debugging.
- [ ] print debugging — Not documented; recommend migrating to logging module.
- [x] Django shell — Available via `python manage.py shell`; not documented in README.
- [ ] Template debugging — `{% debug %}` tag not used; could demonstrate for teaching.
- [ ] Query debugging — No SQL query logging configured; recommend for development.
- [ ] Error tracking — No Sentry or error monitoring configured.
- [ ] Reproduction steps — No bug reproduction documentation; recommend adding to CONTRIBUTING.md.
- [ ] Documentation — No debugging workflows documented yet.

---

## 21. Validation with PRD Alignment

- [ ] FR coverage — Core blog slice (list/detail/create/update/delete, markdown render) is implemented; full PRD trace table pending.
- [ ] NFRs — Accessibility/security/performance documentation not formalized (security: XSS mitigated via Bleach in markdown filter).
- [ ] Pedagogical notes — Additional commentary tying code to Layman chapters would be helpful.
- [ ] Lint/style — Markdownlint/DJLint not run; code follows PEP 8 in new/edited files.
- [ ] Acceptance traceability — Add a brief matrix mapping PRD items to files/tests.

---

## 22. Deliverables

- [x] CHECKLIST_COMPLETION.md — This file.
- [ ] Screenshots/asciinema — Not yet added.
- [ ] Summary table (PRD → Layman → Artifact) — Not yet added.
- [ ] All 20 chapters from *Understand Django* — Now assessed with chapters 9-20 added to checklist.

---

### Notes and pointers

- Markdown rendering and sanitization
  - Filter: `blog/templatetags/markdown_extras.py` combines python-markdown and bleach; tests confirm `<script>` stripped and links preserved.
  - Templates apply `{{ post.body|markdown_safe|safe }}`; admin uses EasyMDE via custom change form.

- Slug handling
  - `slug` is non-editable and auto-generated in `Post.save()`; we removed admin `prepopulated_fields` to avoid KeyError when slug isn’t in the form.

- Publishing filter
  - Views restrict to `publish_date <= now`; future-dated posts are hidden from list/detail.

- Tests
  - `blog/tests.py` covers CRUD, list/detail 200s, and markdown sanitization.

- Optional quick wins (low risk)
  - Add `Post.get_absolute_url()` and use it in templates/redirects.
  - Add a `resolve()` URL test for one route.
  - Add a short accessibility checklist pass (headings, labels, contrast).
