# BRIEF (cpb-0.1.2): Post MVP + Bootstrap base + Markdown editor (admin + public authoring)

PRD Anchor

- docs/blog_site_prd.md §2 “Post MVP” (reader experience + authoring ergonomics)
ADR Anchor
- ADR-0.1.0: Adopt Django for Personal Blog Example MVP

Goal

- Deliver read-only Post list/detail with clean Bootstrap UI, plus public authoring/editing using a textarea enhanced with a Markdown editor (EasyMDE). All rendered HTML must be sanitized.

Scope (single PR; ≲300 LOC)

- Model: Post with fields (title, slug unique, body_markdown, status draft/published, published_at nullable, created_at, updated_at). If already added in 0.1.2, no model changes.
- Admin:
  - Register Post (list_display/search/prepopulated_fields).
  - Keep admin change form EasyMDE via CDN.
- Public authoring (new):
  - ModelForm: PostForm with fields [title, body_markdown, status]. Auto-generate slug from title on save if empty; unique constraint enforced.
  - Views/URLs: PostCreateView at “/compose/”, PostUpdateView at “/posts/<slug>/edit/” (reuse form). Redirect to detail on success.
  - Templates: blog/templates/blog/post_form.html extending base.html; attach EasyMDE to the textarea via CDN.
- Reader views/templating:
  - ListView at “/” (published only, newest first), DetailView at “/posts/<slug>/” (404 for drafts).
  - templates/base.html with Bootstrap 5 (CDN), simple navbar/footer.
  - blog/templates/blog/post_list.html and post_detail.html using Bootstrap components.
- Rendering: Convert Markdown to HTML and sanitize with bleach (allow basic tags).
- Tests: Django TestCase for list/detail visibility, create/edit happy paths, and sanitized rendering.
- Requirements: python deps markdown, bleach (if not already present).
- Non-goals: auth/permissions, images/uploads, tagging, pagination, search.

Standards

- Python 3.12 + Django; PEP 8; docstrings on public functions; type hints on new code.
- CBVs preferred; use ModelForm for Post; no pytest (use Django TestCase).
- Settings: read secrets from environment.

Files to touch (anticipated)

- blog/forms.py (PostForm)
- blog/views.py (PostListView, PostDetailView, PostCreateView, PostUpdateView)
- blog/urls.py (/, /posts/<slug>/, /compose/, /posts/<slug>/edit/)
- blog/templates/blog/post_list.html, post_detail.html, post_form.html
- templates/base.html
- blog/admin.py (ensure registration and change_form_template retained)
- blog/templates/admin/blog/post/change_form.html (EasyMDE for admin)
- project urls.py include for blog
- tests: blog/tests/test_posts.py
- requirements.txt or pyproject.toml (markdown, bleach)

Migration plan

- None if Post model already exists. If adding it now: one migration to create Post with unique slug.

Rollback

- Windows: py manage.py migrate blog zero (if model introduced in this PR)
- Otherwise: git revert <merge-sha> to remove views/urls/templates; delete routes.

Acceptance

- GET / shows published posts with Bootstrap layout (newest first).
- GET /posts/<slug>/ renders post body from Markdown to sanitized HTML (no scripts).
- GET /compose/ shows a form with a Markdown editor toolbar; submitting creates a draft by default and redirects to detail.
- GET /posts/<slug>/edit/ shows the same editor; submitting updates the post and redirects to detail.
- Drafts are excluded from list and 404 on detail unless status=published.

How to Test (local)

1) pip install markdown bleach
2) py manage.py makemigrations && py manage.py migrate
3) py manage.py createsuperuser
4) py manage.py runserver
5) Admin: verify EasyMDE loads on Post change form.
6) Public: visit /compose/, create a draft and a published post; verify EasyMDE loads, redirects work, and sanitized rendering on detail.
7) Tests: py manage.py test blog -v 2

Prompts for Copilot

- Create PostForm (ModelForm) with fields [title, body_markdown, status]; in save(), auto-generate a unique slug from title if missing. Add type hints and docstrings.
- Implement PostCreateView and PostUpdateView (CBVs) using PostForm; success redirect to detail by slug. Wire URLs /compose/ and /posts/<slug>/edit/.
- Build post_form.html extending base.html; include Bootstrap form classes and EasyMDE via CDN (init on #id_body_markdown). Keep CSRF token and error rendering.
- Ensure ListView/DetailView show only published posts; DetailView returns 404 for drafts. Wire urls and templates.
- Add Markdown rendering using markdown + bleach (helper or template filter). Allow tags: ["p","a","code","pre","em","strong","ul","ol","li","h1","h2","h3","blockquote"] and add rel="nofollow noopener".
- Write Django TestCase: create() via client POST to /compose/ creates a draft and redirects; update() via /posts/<slug>/edit/ persists changes; list excludes drafts; detail 404 for drafts; rendered HTML contains expected tags but strips <script>.

Commit message seeds (conventional)

- feat(blog): add PostForm + Create/Update CBVs with EasyMDE
- feat(ui): Bootstrap base and form template for authoring
- feat(blog): sanitize Markdown rendering for detail
- test(blog): cover authoring flows and safe rendering

Risks

- XSS via Markdown (mitigate with bleach allowlist).
- Open authoring without auth (acceptable for MVP); follow-up to add login/permissions.

Links

- PRD §2 • ADR-0.1.0
