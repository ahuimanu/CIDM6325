# BRIEF: Build search functionality tests slice

Goal

- Implement tests for search views, forms, and query logic addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/search/tests.py` or `travelmathlite/apps/search/tests/test_views.py`, `travelmathlite/apps/search/tests/test_search.py`.
- Behavior: Test search form processing, query execution, results rendering; mock external data sources.
- Non-goals: Full-text search engine tuning, performance testing.

Standards

- Commits: conventional style (test).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: Run `uv run python manage.py test search` and see all search tests pass.
- Tests cover search query processing, results display, empty results handling.
- External calls (if any) are mocked.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create tests in `apps/search/tests.py` for search form validation and query processing."
- "Test search view GET and POST requests; verify results are returned for valid queries."
- "Add tests for empty search results and invalid search inputs."
- "Mock any external data sources or API calls used in search functionality."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated)
