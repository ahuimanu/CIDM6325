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

## 9. Validation with PRD Alignment

- [ ] FR coverage — Core blog slice (list/detail/create/update/delete, markdown render) is implemented; full PRD trace table pending.
- [ ] NFRs — Accessibility/security/performance documentation not formalized (security: XSS mitigated via Bleach in markdown filter).
- [ ] Pedagogical notes — Additional commentary tying code to Layman chapters would be helpful.
- [ ] Lint/style — Markdownlint/DJLint not run; code follows PEP 8 in new/edited files.
- [ ] Acceptance traceability — Add a brief matrix mapping PRD items to files/tests.

---

## 10. Deliverables

- [x] CHECKLIST_COMPLETION.md — This file.
- [ ] Screenshots/asciinema — Not yet added.
- [ ] Summary table (PRD → Layman → Artifact) — Not yet added.

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
