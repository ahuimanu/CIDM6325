# BRIEF: Build URL design, canonical, and sitemap slice

Goal

- Establish friendly URL shapes, canonical tags for key pages, and sitemap/robots inclusion addressing PRD §4 F-007 and §10 Acceptance.

Scope (single PR)

- Files to touch: `apps/search/urls.py`, project `core/urls.py` includes, `apps/*/urls.py` as needed, `apps/base/templates/base.html` (or layout) for canonical link block, sitemap/robots configuration.
- Behavior: Ensure `/search/` under `search` namespace; canonical link rel on result pages (e.g., self-referencing with `q` and page); add sitemap entries for search (if applicable) and main pages; update robots if needed.
- Non-goals: API endpoints, content beyond link tags.

Standards

- Commits: conventional style (feat/docs/chore).
- Use `reverse()` in templates for links; avoid hardcoded URLs.
- Keep configuration DB-agnostic and minimal.

Acceptance

- User flow: Navigating to `/search/?q=ABC` shows canonical link in `<head>`, URLs reverse correctly via `url 'search:index'` or similar.
- Sitemap includes primary user-visible pages; robots does not block search results unless specified.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Confirm namespaced `search` URL and add canonical link block in base template with overridable block if needed."
- "Add sitemap entries and ensure they render; update robots.txt if included."
- "Prove links use `reverse()` in templates; add a small smoke test."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §4 F-007; §10 Acceptance
Requirements: FR-F-007-1
