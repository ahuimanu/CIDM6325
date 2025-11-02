# BRIEF: Build Blog Post CRUD & Model Slice

Goal  
- Implement blog post CRUD (Create, Read, Update, Delete) and core model per PRD §4, §6, and ADR-0.1.0.

Scope (single PR)  
- Files to touch:  
  - `blog/models.py`: Post model (slug, title, body [Markdown], publish_date, tags).
  - `blog/forms.py`: Post ModelForm.
  - `blog/views.py`: CBVs for List, Detail, Create, Update, Delete.
  - `blog/urls.py`: URL patterns for CRUD views.
  - `blog/templates/blog/`: Templates for list, detail, form.
  - `blog/tests.py`: Django TestCase for model and views.
  - Migration file for Post model.

- Non-goals:  
  - No search, feeds, sitemap, SEO, robots.txt.
  - No multi-author, comments, API, advanced front-end.

Standards  
- Commits: conventional style (feat/fix/docs/refactor/chore).
- PEP 8, docstrings on public functions, type hints on new code.
- Django CBVs for CRUD; ModelForm for post.
- Migrations: one logical change (Post model).
- Django TestCase (no pytest).
- Settings: secrets via environment (not needed for this slice).

Acceptance  
- User flow:  
  1. Author can create, edit, delete posts via web UI.
  2. Visitors can view list and detail pages.
  3. Markdown body renders safely.
  4. All actions redirect appropriately.
  5. Unit tests for model and views pass.

- Include migration? yes  
- Update docs & PR checklist: yes

Prompts for Copilot  
- "Generate Django Post model with slug, title, body (Markdown), publish_date, tags."
- "Create ModelForm for Post."
- "Implement CBVs for Post CRUD with success redirects."
- "Draft URL patterns for CRUD views."
- "Scaffold templates for list, detail, and form."
- "Write Django TestCase for Post model and CRUD views."
- "Propose atomic commit messages for each file."