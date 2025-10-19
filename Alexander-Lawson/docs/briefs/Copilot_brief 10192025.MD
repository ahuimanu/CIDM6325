# BRIEF: Build template inheritance & CBV refactor slice

Goal

- Implement template inheritance by creating a base template (`base.html`) for the blog.
- Incorporate Bootstrap 5.3 via CDN in `base.html` for responsive design.
- Refactor existing function-based views (FBVs) to class-based views (CBVs).

Scope (single PR)

- Files to touch:
  - `templates/base.html` – Create base template with Bootstrap 5.3 CDN.
  - `templates/blog/*.html` – Update templates to extend `base.html`.
  - `blog/views.py` – Refactor FBVs to CBVs.
  - `blog/urls.py` – Update URL patterns if needed for CBVs.
- Non-goals:
  - Adding new features or endpoints.
  - Custom Bootstrap theming beyond CDN inclusion.

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance

- User flow: All blog pages use the new base template for consistent layout and Bootstrap styling. All views previously implemented as FBVs now use CBVs with identical behavior.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create a Django base template with Bootstrap 5.3 CDN and block structure for inheritance."
- "Refactor function-based views in blog/views.py to class-based views; update urls.py as needed."
- "Update blog templates to extend base.html and use Bootstrap classes."
- "Explain changes and propose commit messages."
- "Generate unit tests for refactored CBVs."