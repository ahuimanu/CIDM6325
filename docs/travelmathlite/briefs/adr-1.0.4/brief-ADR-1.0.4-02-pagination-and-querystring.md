# BRIEF: Build pagination and querystring preservation slice

Goal

- Add pagination to search results and preserve `q` across page links addressing PRD §4 F-008.

Scope (single PR)

- Files to touch: `apps/search/views.py` (Paginator integration), `apps/search/templates/search/results.html` (pagination controls), optional template tag/helper for querystring building.
- Behavior: Use `Django Paginator`; expose `page_obj`; ensure pagination links include escaped `q` and current page.
- Non-goals: highlight rendering (separate), URL canonicalization (separate).

Standards

- Commits: conventional style (feat/test/docs).
- Use `uv run` to execute tests/server; lint/format with Ruff.
- Django tests with TestCase: assert presence of pagination controls and preserved query string.

Acceptance

- User flow: `GET /search/?q=LAX&page=2` returns page 2 of results with correct counts and functional next/prev links.
- Invariant: Pagination links preserve the escaped `q` (INV-1 from ADR).
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Integrate `Paginator` in `SearchView` to paginate `results`, passing `page_obj` to the template."
- "Update template to render first/prev/next/last with `q` preserved in the query string."
- "Write tests to confirm `q` persists across pagination links and page numbers."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §4 F-008; §10 Acceptance
Requirements: FR-F-008-1
