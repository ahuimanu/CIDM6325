# Django Blog PRD Alignment Checklist
## Consistency with *Understand Django* (Matt Layman, Chapters 1–8)
This checklist ensures that the Django Blog Example (per the PRD) fulfills pedagogical and structural
expectations aligned with Matt Layman’s *Understand Django* series (Chs. 1–8: *From Browser to Django*).
Each section connects the implementation deliverables from the PRD to the conceptual grounding in Layman’s work.

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
  ```
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

## 10. Deliverables
- [ ] `CHECKLIST_COMPLETION.md` included in repo root, checked off by instructor/student.
- [ ] Screenshots or asciinema clips showing each milestone.
- [ ] Final summary table mapping PRD → Layman Ch. X → Verified artifact.

---

**References**
- Matt Layman, *Understand Django* (<https://www.mattlayman.com/understand-django/>)
- Django 5.x Documentation (<https://docs.djangoproject.com/en/5.0/>)
- Django Blog Example PRD (rev 0.1, 2025-10-07)
- Carlton Gibson’s noumenal.es (structural reference)