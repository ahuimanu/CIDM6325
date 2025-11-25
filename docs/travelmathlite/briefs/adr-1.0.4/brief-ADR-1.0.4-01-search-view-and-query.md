# BRIEF: Build search view and query parsing slice

Goal

- Implement basic airport/city search view with safe query parsing addressing PRD §4 F-008 and F-007.

Scope (single PR)

- Files to touch: `travelmathlite/apps/search/views.py`, `travelmathlite/apps/search/urls.py`, `travelmathlite/apps/search/templates/search/results.html`, navbar partial if present.
- Behavior: parse `q` from GET, guard empty queries, case-insensitive `icontains` against key fields (airport/city name, IATA/ident where applicable), return a `QuerySet` suitable for pagination.
- Non-goals: pagination links (separate), highlight rendering (separate), fuzzy matching.

Standards

- Commits: conventional style (feat/test/docs).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest). Autoescape remains on in templates.

Acceptance

- User flow: `GET /search/?q=ABC` returns HTTP 200 with results context when `q` is non-empty; empty `q` yields an informative response (no crash) and no DB query.
- Query parsing escapes user input and trims whitespace; invalid/very long `q` is safely handled.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create `SearchView` (CBV) that reads `q` from GET, validates non-empty, escapes it, and prepares a `results` queryset filtered via `icontains` across airport/city fields."
- "Wire `apps/search/urls.py` with namespaced `app_name = 'search'` and path `''` named `index` or `results`."
- "Render a minimal template showing count and first page placeholder (pagination added later)."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §4 F-008; §10 Acceptance
Requirements: FR-F-008-1, FR-F-007-1, NF-003
