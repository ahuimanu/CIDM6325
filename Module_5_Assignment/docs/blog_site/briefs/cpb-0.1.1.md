# BRIEF: Refactor Blog CRUD to CBVs & Bootstrap Base Template

Goal  
- Refactor blog CRUD views to use Django class-based views (CBVs).
- Implement template inheritance with a new `base.html`.
- Integrate Bootstrap 5.3 via CDN in `base.html` for simple styling.

Scope (single PR)  
- Files to touch:  
  - `blog/views.py`: Refactor all CRUD views to CBVs (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).
  - `blog/templates/blog/base.html`: New base template with Bootstrap 5.3 CDN.
  - `blog/templates/blog/post_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`: Refactor to extend `base.html`.
  - `blog/urls.py`: Update to use CBV as_view() methods.
  - `blog/tests.py`: Update or add tests for CBVs. (not covered until Chapter 12, so optional)

- Non-goals:  
  - No custom Bootstrap theming.
  - No advanced template blocks or navigation.
  - No changes to model or form logic.

Standards  
- Commits: conventional style (feat/refactor/docs/test).
- PEP 8, docstrings on public functions, type hints on new code.
- Use Django CBVs for all CRUD endpoints.
- Templates must use `{% extends "blog/base.html" %}` and `{% block content %}`.
- Bootstrap 5.3 loaded via CDN in `base.html`.

Acceptance  
- All blog pages render with Bootstrap styling.
- All views use CBVs and function as before.
- Templates inherit from `base.html`.
- Unit tests for CBVs pass.

- Include migration? no  
- Update docs & PR checklist: yes

Prompts for Copilot  
- "Refactor blog CRUD views to CBVs with success redirects."
- "Create base.html with Bootstrap 5.3 CDN and content block."
- "Update all templates to extend base.html and use block content."
- "Update urls.py to use CBV as_view()."
- "Write/adjust Django TestCase for CBVs."
- "Propose atomic commit messages for each file."