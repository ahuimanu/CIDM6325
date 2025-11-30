# BRIEF (cpb-0.1.4): Search with Pagination

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §4 In Scope F-005; §5 FR-F-004-1; §10 Acceptance

ADR Anchor

- ADR-0.1.0 (Django MVP)

Goal

- Implement simple full-text search over Post title/body with result pagination.

Scope (single PR; ≲300 LOC)

- Query param `q` filters published posts (case-insensitive contains on title/body).
- Add a dedicated SearchView (CBV) and template with pagination (e.g., 10/page).
- Show match count and highlight snippets (wrap matched terms with a highlight span/class).
- Link to search from navbar; preserve `q` across pagination.
- Tests: Search happy path, empty query fallback, pagination, and HTML escaping.

Standards

- Python 3.12 + Django; PEP 8; docstrings and type hints on new code.
- Avoid heavy search deps; use ORM icontains for MVP.

Files to touch (anticipated)

- blog/views.py (SearchView)
- blog/urls.py (add /search/)
- blog/templates/blog/search_results.html
- blog/templates/blog/base.html (add search form in navbar)
- blog/tests.py (search tests)

Migration plan

- None.

Rollback

- git revert merge commit; remove search view/urls/templates.

Acceptance

- GET /blog/search/?q=foo returns a paginated list of published posts matching title/body.
- Empty or missing q shows zero-state page with guidance.
- Pagination works and preserves the query parameter.
- Snippets highlight matched query terms without breaking HTML.

How to Test (local)

1) Create multiple posts with varying titles/bodies including the term you’ll search for.
2) Visit /blog/search/?q=term and navigate pages.
3) Run tests: py manage.py test blog -v 2

Prompts for Copilot

- Add SearchView using ListView + get_queryset() filtering title__icontains | body__icontains for published posts.
- Wire urlpattern “search/” with name="post_search"; add a search form to navbar submitting to that route (GET).
- Create search_results.html with pagination controls and snippet highlighting (replace matched terms with a span.highlight around the text; ensure output is escaped before marking safe).
- Write tests for search filtering, pagination, and escaping.
