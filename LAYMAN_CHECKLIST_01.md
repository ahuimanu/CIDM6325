# Django Blog PRD Alignment Checklist

## Consistency with *Understand Django* (Matt Layman, All 20 Chapters)

This checklist ensures that the Django Blog Example (per the PRD) fulfills pedagogical and structural
expectations aligned with Matt Layman's complete *Understand Django* series (Chapters 1–20).
Each section connects the implementation deliverables from the PRD to the conceptual grounding in Layman's work,
from foundational concepts (*From Browser to Django*) through advanced topics (deployment, performance, security, debugging).

---

## 1. From Browser to Django (Introductory Context)

- [ ] **HTTP request/response flow**: Demonstrate how a browser request reaches Django via URLs → views → templates.
- [ ] **Runserver demonstration**: Show `python manage.py runserver` and access to `/` and `/posts/`.
- [ ] **Console inspection**: Log request path and response codes in development server output.
- [ ] **Code commentary**: Annotate early views with docstrings referencing Django’s request/response cycle.
- [ ] **Visual diagram (optional)**: Include diagram mapping Browser → Django → Template → HTML Response.

---

## 2. URLs Lead the Way

- [ ] **urls.py created** with `urlpatterns` defining `path("", views.post_list, name="post_list")` and `path("posts/<slug:slug>/", views.post_detail, name="post_detail")`.
- [ ] **Namespace clarity**: App-level `urls.py` included under project `urls.py` with `include("blog.urls")`.
- [ ] **URL naming discipline**: All routes use `name=` for reverse resolution in templates.
- [ ] **Canonical link alignment**: `post_detail` URL pattern aligns with PRD canonical URL requirements.
- [ ] **Test coverage**: `reverse()` and `resolve()` verified for core routes.

---

## 3. Views on Views

- [ ] **Function-based views (FBVs)** defined for list/detail; optional refactor to class-based views (CBVs) as second phase.
- [ ] **Proper use of `HttpResponse`/`render()`** for returning HTML responses.
- [ ] **View docstrings** reference Matt Layman’s “views mediate between model and template” guidance.
- [ ] **Error handling**: `get_object_or_404()` used for missing posts.
- [ ] **Unit tests**: Basic tests for status 200 on home and detail pages.

---

## 4. Templates for User Interfaces

- [ ] **Templates directory** configured correctly in `settings.py` (`DIRS`, `APP_DIRS`).
- [ ] **Base template** with `{% block content %}` and `{% extends "base.html" %}` in all pages.
- [ ] **List/detail templates** render `{{ post.title }}`, `{{ post.body|safe }}`, and formatted dates.
- [ ] **Template tags**: Use `{% url "post_detail" slug=post.slug %}` for internal links.
- [ ] **Markdown rendering verified** with safe HTML sanitization (PRD FR-002).
- [ ] **Accessibility compliance**: Headings, alt text, semantic HTML validated.

---

## 5. User Interaction with Forms

- [ ] **Form created** (`forms.py`) for authoring/editing posts or for a “Contact/Feedback” example.
- [ ] **CSRF token** present in template forms.
- [ ] **Validation handled** with Django’s `clean_` methods or field validators.
- [ ] **Form lifecycle demonstrated**: GET shows form; POST processes submission → redirect pattern.
- [ ] **Optional enrichment**: Include model form pattern (`ModelForm`) and `commit=False` save example.

---

## 6. Store Data with Models

- [ ] **Post model** implemented per PRD: `title`, `slug`, `body`, `published_at`, `tags`.
- [ ] **Database migration** created and applied via `python manage.py makemigrations` / `migrate`.
- [ ] **Admin entry** created for `Post`.
- [ ] **Slug uniqueness enforced** with `unique_for_date` or custom `save()` logic.
- [ ] **Model methods**: `get_absolute_url()` returns canonical route for posts.
- [ ] **ORM queries** used in views (`Post.objects.filter(...)`)—no raw SQL.
- [ ] **Tests verify persistence**: create → retrieve → delete sequence passes.

---

## 7. Administer All the Things

- [ ] **Admin site enabled** with superuser creation.
- [ ] **Custom `ModelAdmin`** for `Post` includes `list_display`, `prepopulated_fields` for slug.
- [ ] **Markdown preview integration** optional or documented (for teaching extension).
- [ ] **Permissions model** simplified: single author workflow, staff-only edit access.
- [ ] **Screenshots/documentation** demonstrate admin use as per Layman’s “Admin” chapter context.
- [ ] **Test coverage**: admin route accessible only to authenticated user.

---

## 8. Anatomy of an Application

- [ ] **App layout** follows Django convention:
  
  ```text
  blog/
      __init__.py
      admin.py
      apps.py
      forms.py
      migrations/
      models.py
      templates/blog/
      tests.py
      urls.py
      views.py
  ```

- [ ] **Settings module** isolates environment configs (`settings/base.py`, `dev.py`, `prod.py` optional).
- [ ] **`INSTALLED_APPS`** includes `'blog'` explicitly.
- [ ] **Static files** served through Whitenoise or collectstatic pipeline.
- [ ] **Project README** maps folder structure to “Anatomy” explanations.
- [ ] **Students can navigate** each layer (URLs → Views → Templates → Models → Admin) confidently.

---

## 9. Validation with PRD Alignment

- [ ] Each functional requirement (FR-001 – FR-009) demonstrably satisfied within the chapter progression.
- [ ] Non-functional targets (performance, accessibility, security) validated in docs/tests.
- [ ] Clear pedagogical commentary linking code to Layman’s conceptual framing.
- [ ] Markdownlint and DJLint pass; code style matches PEP 8 and project lint rules.
- [ ] PRD acceptance criteria met and traceable through this checklist.

---

## 9. User Authentication

- [ ] **Authentication system enabled** (`django.contrib.auth` in `INSTALLED_APPS`).
- [ ] **Login/Logout views** configured using `LoginView`, `LogoutView` from `django.contrib.auth.views`.
- [ ] **User registration** optional: include signup form or document third-party packages (e.g., `django-allauth`).
- [ ] **Login required decorator** applied to views that require authentication (`@login_required`).
- [ ] **User permissions** demonstrated: staff vs regular users, custom permissions optional.
- [ ] **Password management**: Include password reset flow or document Django's built-in views.
- [ ] **Templates**: Login/logout templates styled consistently with base template.
- [ ] **Tests**: Verify login redirects, logout clears session, protected views require auth.

---

## 10. Middleware Do You Go?

- [ ] **Middleware stack** reviewed in `settings.py` (`MIDDLEWARE` list).
- [ ] **Custom middleware** created (optional): example logging middleware or request timer.
- [ ] **Middleware order** documented: explain importance of ordering (security → session → auth).
- [ ] **Common middleware explained**: SecurityMiddleware, SessionMiddleware, AuthenticationMiddleware, CsrfViewMiddleware.
- [ ] **Process request/response hooks** demonstrated in custom middleware.
- [ ] **Exception handling**: Document middleware's role in catching exceptions.
- [ ] **Tests**: Custom middleware behavior verified with test requests.

---

## 11. Serving Static Files

- [ ] **Static files configuration** in `settings.py`: `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`.
- [ ] **Static directory structure**: `blog/static/blog/` for app-specific assets.
- [ ] **Template integration**: Use `{% load static %}` and `{% static 'blog/style.css' %}` in templates.
- [ ] **Development serving**: `django.contrib.staticfiles` in `INSTALLED_APPS`.
- [ ] **Production strategy**: Document `collectstatic` command and CDN options.
- [ ] **Whitenoise integration** (optional): Configure for serving static files in production.
- [ ] **Assets verified**: CSS, JS, images load correctly in both dev and production modes.
- [ ] **Tests**: Static file URLs resolve correctly.

---

## 12. Test Your Apps

- [ ] **Test suite created**: `tests.py` or `tests/` directory with test modules.
- [ ] **Django TestCase** used (not pytest, per project norms).
- [ ] **Model tests**: Create, retrieve, update, delete operations verified.
- [ ] **View tests**: Status codes, template usage, context data validated.
- [ ] **Form tests**: Valid/invalid data submissions tested.
- [ ] **URL tests**: `reverse()` and `resolve()` tested for all routes.
- [ ] **Coverage target**: Aim for >80% code coverage (document with `coverage.py`).
- [ ] **Test data**: Use fixtures or factory patterns for consistent test data.
- [ ] **CI integration** (optional): Tests run automatically on push (GitHub Actions).
- [ ] **Documentation**: Testing strategy and run instructions in README.

---

## 13. Deploy A Site Live

- [ ] **Deployment target selected**: Document platform (Heroku, Railway, PythonAnywhere, VPS).
- [ ] **Environment variables**: Secrets managed via `.env` or platform config (not hardcoded).
- [ ] **Database configured**: PostgreSQL or production-appropriate database (not SQLite in prod).
- [ ] **Static files served**: `collectstatic` run, files served via CDN or Whitenoise.
- [ ] **ALLOWED_HOSTS** configured correctly for production domain.
- [ ] **DEBUG = False** in production settings.
- [ ] **HTTPS enforced**: SSL certificate configured, SECURE_SSL_REDIRECT enabled.
- [ ] **Deployment checklist**: Django's deployment checklist run (`python manage.py check --deploy`).
- [ ] **Monitoring**: Error tracking configured (Sentry optional).
- [ ] **Documentation**: Deployment steps and rollback procedures documented.

---

## 14. Per-visitor Data With Sessions

- [ ] **Session middleware** enabled in `MIDDLEWARE` (default).
- [ ] **Session backend** configured: database-backed or cache-backed sessions.
- [ ] **Session data usage**: Example view storing/retrieving session data (`request.session['key']`).
- [ ] **Session expiration**: Configure `SESSION_COOKIE_AGE` and `SESSION_EXPIRE_AT_BROWSER_CLOSE`.
- [ ] **Security settings**: `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` enabled in production.
- [ ] **Session cleanup**: Document `clearsessions` management command for database sessions.
- [ ] **Use cases demonstrated**: Shopping cart, preferences, multi-step forms.
- [ ] **Tests**: Session persistence and expiration tested.

---

## 15. Making Sense Of Settings

- [ ] **Settings organization**: Single `settings.py` or split into `base.py`, `dev.py`, `prod.py`.
- [ ] **Environment-specific configs**: Use `os.environ.get()` or `django-environ` for environment variables.
- [ ] **Secret key management**: Never commit `SECRET_KEY` to version control.
- [ ] **Database configuration**: Different databases for dev (SQLite) and prod (PostgreSQL).
- [ ] **Debug mode**: `DEBUG = True` in dev, `False` in prod.
- [ ] **Logging configuration**: `LOGGING` dict configured for appropriate verbosity.
- [ ] **Email backend**: Configured for dev (console) and prod (SMTP/service).
- [ ] **Settings documentation**: Document all custom settings and their purposes.
- [ ] **Validation**: Use `check` framework for custom settings validation.

---

## 16. User File Use (Media Files)

- [ ] **Media files configuration**: `MEDIA_URL` and `MEDIA_ROOT` set in settings.
- [ ] **File upload field**: Example model with `FileField` or `ImageField`.
- [ ] **Development serving**: `urlpatterns += static(settings.MEDIA_URL, ...)` in dev URLs.
- [ ] **Production serving**: Document CDN (S3, Cloudinary) or web server (Nginx) strategy.
- [ ] **File validation**: Validate file types and sizes on upload.
- [ ] **Storage backends**: Document `DEFAULT_FILE_STORAGE` for production (e.g., `django-storages`).
- [ ] **Security**: Prevent directory traversal, validate extensions, use UUIDs for filenames.
- [ ] **User experience**: Display uploaded files (images) in templates.
- [ ] **Tests**: File upload and retrieval tested.

---

## 17. Command Your App (Management Commands)

- [ ] **Custom management command** created in `blog/management/commands/`.
- [ ] **Command structure**: Inherits from `BaseCommand`, implements `handle()` method.
- [ ] **Command arguments**: Use `add_arguments()` for CLI args (optional flags, positional args).
- [ ] **Use cases**: Data import, cleanup tasks, scheduled jobs, reports.
- [ ] **Output styling**: Use `self.stdout.write(self.style.SUCCESS(...))` for colored output.
- [ ] **Error handling**: Catch exceptions, provide helpful error messages.
- [ ] **Documentation**: Command purpose, arguments, and usage examples in docstrings/README.
- [ ] **Tests**: Command execution tested with `call_command()`.
- [ ] **Automation**: Document how to schedule commands (cron, Celery, etc.).

---

## 18. Go Fast With Django (Performance)

- [ ] **Database query optimization**: Use `select_related()` and `prefetch_related()` to reduce queries.
- [ ] **Query analysis**: Use Django Debug Toolbar to identify N+1 queries.
- [ ] **Indexing strategy**: Database indexes on frequently queried fields (foreign keys, filtering fields).
- [ ] **Caching implemented**: View caching, template fragment caching, or queryset caching.
- [ ] **Cache backend configured**: Redis or Memcached for production (not in-memory).
- [ ] **Static file optimization**: Minify CSS/JS, use CDN, enable browser caching.
- [ ] **Database connection pooling**: Configure for production (e.g., `django-db-geventpool`).
- [ ] **Pagination**: Implement for list views to limit query size.
- [ ] **Performance testing**: Use `django-silk` or similar to profile views.
- [ ] **Documentation**: Performance optimization strategies and benchmarks documented.

---

## 19. Security And Django

- [ ] **Security settings enabled**: `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`.
- [ ] **XSS protection**: Template auto-escaping enabled, use `|safe` sparingly and correctly.
- [ ] **CSRF protection**: CSRF middleware enabled, tokens in all forms.
- [ ] **SQL injection prevention**: Use ORM, never raw SQL with string interpolation.
- [ ] **Clickjacking protection**: `X-Frame-Options` via `XFrameOptionsMiddleware`.
- [ ] **Content Security Policy** (optional): Configure CSP headers.
- [ ] **Dependency management**: Keep Django and dependencies updated, monitor security advisories.
- [ ] **Password strength**: Use Django's password validators, enforce minimum complexity.
- [ ] **User input validation**: Validate all user input, sanitize file uploads.
- [ ] **Security audit**: Run `python manage.py check --deploy` and address warnings.
- [ ] **Penetration testing** (optional): Document security testing approach.
- [ ] **Documentation**: Security measures and incident response plan documented.

---

## 20. Debugging Tips And Techniques

- [ ] **Django Debug Toolbar installed** (dev only): Configure to show queries, templates, signals.
- [ ] **Logging configured**: Use Python's `logging` module, configure log levels appropriately.
- [ ] **Error pages**: Custom 404/500 templates created for production.
- [ ] **Development debugging**: Use `breakpoint()` or `pdb` for interactive debugging.
- [ ] **VS Code debugging** (optional): Configure launch.json for Django debugging.
- [ ] **print debugging**: Use `print()` statements strategically or migrate to logging.
- [ ] **Django shell**: Use `python manage.py shell` for interactive testing.
- [ ] **Template debugging**: Use `{% debug %}` tag to inspect context (dev only).
- [ ] **Query debugging**: Log SQL queries in dev, use `connection.queries` for analysis.
- [ ] **Error tracking**: Sentry or similar service for production error monitoring.
- [ ] **Reproduction steps**: Document how to reproduce bugs for easier debugging.
- [ ] **Documentation**: Debugging workflows and common issues documented in CONTRIBUTING.md.

---

## 21. Validation with PRD Alignment

- [ ] Each functional requirement (FR-001 – FR-009) demonstrably satisfied within the chapter progression.
- [ ] Non-functional targets (performance, accessibility, security) validated in docs/tests.
- [ ] Clear pedagogical commentary linking code to Layman's conceptual framing.
- [ ] Markdownlint and DJLint pass; code style matches PEP 8 and project lint rules.
- [ ] PRD acceptance criteria met and traceable through this checklist.

---

## 22. Deliverables

- [ ] `CHECKLIST_COMPLETION.md` included in repo root, checked off by instructor/student.
- [ ] Screenshots or asciinema clips showing each milestone.
- [ ] Final summary table mapping PRD → Layman Ch. X → Verified artifact.
- [ ] All 20 chapters from *Understand Django* represented and checked off.

---

### References

- Matt Layman, *Understand Django* (<https://www.mattlayman.com/understand-django/>)
  - Complete 20-chapter series covering Django from basics to advanced topics
- Django 5.x Documentation (<https://docs.djangoproject.com/en/5.0/>)
- Django Blog Example PRD (rev 0.1, 2025-10-07)
- Carlton Gibson's noumenal.es (structural reference)
- Django Deployment Checklist (<https://docs.djangoproject.com/en/stable/howto/deployment/checklist/>)
