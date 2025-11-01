# CIDM 6325 — Weeks 9–10 Unified Assignment
**Author:** Melodi Parton  
**Course:** CIDM 6325  
**Branch:** `feature/cbv-weeks-7-8`  
**Date:** (update to today)

---

## 1. Purpose

These two weeks focused on adding *production-ish* admin and authentication to the existing Django blog app so that it looks like a real business tool, not just CRUD. The work connects to Layman, **_Understand Django_**, ch. 9 (“Administer All the Things”) and ch. 11 (“User Authentication”).

Deliverables from the prompt:

1. **Part A – Django Admin Implementation 
2. **Part B – Authentication 
3. **Part C – Peer Review 
4. **Part D – Blog Post: Productivity vs Security 
5. **Part E – Static/Uploaded Files 

This document explains what I actually built in my repo.

---

## 2. Part A – Django Admin Implementation

**What I had:** blog app with `Post` model:

- `title`
- `slug`
- `author` (FK to `auth.User`)
- `body`
- `status` (`draft` / `published`)
- `published_at` (nullable)
- `created_at` (auto add)
- `updated_at` (auto now)
- later: `image` (ImageField)

**What I did:**

- Enabled Django admin (already on at `/admin/`).
- Registered the blog model in **`blog/admin.py`** with real customizations.

**Admin code (summary):**

- `list_display = ("title", "author", "status", "published_at", "created_at")`
- `list_filter = ("status", "published_at", "created_at")`
- `search_fields = ("title", "body")`
- `raw_id_fields = ("author",)`
- `date_hierarchy = "published_at"`
- `ordering = ("-published_at", "-created_at")`

**Business use cases (what this gets me):**

1. **Dispatcher/blog manager can quickly see only published items** → filter by status.
2. **Can search for a post by title or content** → search_fields.
3. **Can filter by date** → date_hierarchy, especially for audit or “what did we post last week?”
4. **Author field is raw ID so admin page loads faster** when there are many users.

**Second model for the ‘two models’ requirement:**

- I registered **`auth.User`** in admin with a *safe* customization (view/search).  
- I did **not** try to make a full custom user; I only exposed the user model in admin so I can see who is creating blog posts.

**Screens verified:**

- `/admin/` shows **Authentication and Authorization** (Groups, Users)
- `/admin/blog/post/` shows the customized list
- Filters for **By status**, **By published at**, **By created at** appeared on the right

---

## 3. Part B – Authentication

**Goal from prompt:** “Implement user registration, login, logout. Apply at least one role-based permission check. Document security/usability.”

**What I wired:**

1. **URLs** in `core/urls.py`:

   - `path("accounts/", include("django.contrib.auth.urls"))`  
     → this gives me login, logout, password change, etc.
   - `path("accounts/register/", core_views.register, name="register")`  
     → my own registration view
   - **Special case**: Firefox was returning **405 Method Not Allowed** when I hit  
     `http://127.0.0.1:8000/accounts/logout/`  
     So we added a **GET-friendly logout**:
     ```python
     path(
         "accounts/logout/",
         core_views.GetLogoutView.as_view(),
         name="logout",
     )
     ```
     This forced logout to accept GET and redirect.

2. **Templates** in `templates/registration/`:
   - `login.html`
   - `register.html`
   - `logged_out.html`
   All of them extend **`templates/base.html`** so I can show a top bar with:  
   - “Hi {{ user.username }} | Log out | Blog” (when logged in)  
   - “Log in | Blog” (when anonymous)

3. **Views** in `core/views.py`:
   - `register(request)` → wraps Django’s `UserCreationForm`
   - `GetLogoutView` → subclass of Django logout that accepts GET and redirects to blog list

4. **Settings** in `core/settings.py`:
   ```python
   LOGIN_URL = "login"
   LOGIN_REDIRECT_URL = "blog:post_list"
   LOGOUT_REDIRECT_URL = "blog:post_list"
