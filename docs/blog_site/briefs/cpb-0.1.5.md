# BRIEF (cpb-0.1.5): Static Pages (About, Projects)

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §4 In Scope F-006; §5 FR-F-005-1; §10 Acceptance

ADR Anchor

- ADR-0.1.0 (Django MVP)

Goal

- Add a couple of static pages (About, Projects) rendered via Django templates.

Scope (single PR; ≲200 LOC)

- Use simple TemplateView classes or minimal FBVs for two pages.
- Templates: blog/templates/blog/about.html, projects.html extending base.
- Navbar links to these pages; highlight current page.
- Optional: use Django FlatPages for teachable contrast; start with TemplateViews for simplicity.
- Tests: 200 status on each page; template extends base; basic content asserts.

Standards

- Python 3.12 + Django; PEP 8; docstrings on new views.

Files to touch (anticipated)

- blog/views.py (AboutView, ProjectsView)
- blog/urls.py (routes for /about/ and /projects/)
- blog/templates/blog/about.html, projects.html
- blog/templates/blog/base.html (navbar links)
- blog/tests.py (static page tests)

Migration plan

- None.

Rollback

- git revert merge commit; remove views/urls/templates for static pages.

Acceptance

- GET /blog/about/ and /blog/projects/ return 200 and render expected content.
- Navbar links visible and active state reflected when on that page.

How to Test (local)

1) py manage.py runserver
2) Visit /blog/about/ and /blog/projects/
3) Run tests: py manage.py test blog -v 2

Prompts for Copilot

- Implement TemplateView classes (AboutView, ProjectsView) with templates.
- Wire URL patterns and add navbar links in base template.
- Write basic tests ensuring each page returns 200 and uses the right template.
