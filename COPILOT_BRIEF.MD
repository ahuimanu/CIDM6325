# BRIEF: Build Blog Page Display slice

Goal

- Implement blog page display functionality addressing core blog viewing requirements.

Scope (single PR)

- Files to touch: blog/views.py, blog/urls.py, templates/blog/post_list.html, templates/blog/post_detail.html, blog/tests.py
- Non-goals: User authentication, commenting system, admin interface customizations

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance

- User flow: User visits homepage → sees list of published blog posts → clicks on post title → views full post detail page with proper navigation back to list
- Include migration? no (models already exist)
- Update docs & PR checklist.

Prompts for Copilot

- "Generate a Django ListView for blog posts with pagination and filtering by status=published"
- "Create a DetailView for individual blog posts with slug-based URLs"
- "Design responsive templates using Bootstrap with proper semantic HTML and accessibility attributes"
- "Add URL patterns for blog list and detail views with named URLs"
- "Write unit tests for both views ensuring proper status filtering and 404 handling"
- "Explain changes and propose commit messages."
