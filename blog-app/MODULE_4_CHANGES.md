Module 4 Changes

This document summarizes the code and documentation changes made in Module 4 to satisfy the assignment requirements: refactor a CRUD feature into a Class-Based View (CBV), demonstrate mixin and inheritance use, and document tradeoffs between FBVs and CBVs. It also lists how to verify the changes by running tests and starting the app.

What was changed

1) Refactored Create (CRUD) to a Class-Based View
- File: `blog/views.py`
  - Added `PostCreateView`, a CBV subclassing `LoginRequiredMixin` and Django's `CreateView`.
  - `PostCreateView` uses the existing `PostForm` and the same template `blog/post_form.html` so the UI and validation remain unchanged.
- File: `blog/urls.py`
  - Updated the `posts/new/` route to point to `PostCreateView.as_view()` instead of the previous `post_create` function-based view.

Why: this demonstrates converting a Week 5–6 FBV CRUD endpoint into a CBV, showing how Django's generic class views reduce boilerplate for common CRUD operations.

2) Demonstrated mixin and inheritance
- File: `blog/views.py`
  - Added `AuthorAssignMixin`: a small reusable mixin that centralizes the behavior of assigning the current request.user as the `author` when saving a form.
  - `PostCreateView` composes `LoginRequiredMixin` (built-in) and `AuthorAssignMixin` to show mixin-based reuse and inheritance.

Why: putting author-assignment logic into a mixin removes duplication, clarifies intent, and shows how CBVs can be extended using composition via mixins.

3) Kept behavior and validation intact
- File: `blog/forms.py` (unchanged)
  - `PostForm` and `CommentForm` remain the source of validation and parsing (e.g., `tags_csv` parsing and banned-word checks). The CBV uses the same form API (`form.save(author=...)`) via the mixin.

4) Documentation added and tradeoffs discussed
- File: `APPLICATION_ARCHITECTURE_CRITIQUE.md`
  - A 2–3 page human-readable critique of Django app organization was added.
- The tradeoffs between FBVs and CBVs were documented in earlier messages and summarized in the code comments and critique file: FBVs are explicit and simple; CBVs reduce boilerplate and encourage reuse via mixins but can be harder to read at a glance.

Verification steps (how to confirm everything works)

From the project root (`blog-app`), use PowerShell commands (or your preferred shell) to run tests and start the server.

1) Run tests

```powershell
.venv\Scripts\python.exe manage.py test --verbosity=2
```

Expected: All tests pass (the suite contains 13 tests in this project). I ran this command and saw `OK`.

2) Start the dev server and smoke-test

```powershell
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Then visit in a browser:
- Home / posts list: http://127.0.0.1:8000/
- New post (requires login): http://127.0.0.1:8000/posts/new/
- Dev helper (creates & logs in a dev user when DEBUG=True): http://127.0.0.1:8000/dev-login/ (username `dev`, password `devpass` if created)

Expected: The server starts cleanly; GET / returns 200; navigating to `/posts/new/` when logged in shows the same `post_form.html` form as before and allowed submissions create posts with the logged-in user set as the author.

Files changed (concise list)
- Modified: `blog/views.py` — added `AuthorAssignMixin` and `PostCreateView`.
- Modified: `blog/urls.py` — `posts/new/` mapped to `PostCreateView`.
- Added: `APPLICATION_ARCHITECTURE_CRITIQUE.md` — architecture critique for the assignment.
- Added: `MODULE_4_CHANGES.md` (this file) — summary of Module 4 work.

Notes and suggestions

- The original FBV `post_create` remains in `blog/views.py` for reference and backward compatibility in case other code depends on it. If you prefer, I can remove it to avoid dead code.
- If you want more CBV refactors, I can convert `post_update` and `post_delete` into `UpdateView` and `DeleteView` respectively and introduce a `PostPermissionMixin` that centralizes author-or-permission checks.
