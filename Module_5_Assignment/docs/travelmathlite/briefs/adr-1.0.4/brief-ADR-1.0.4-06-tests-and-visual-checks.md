# BRIEF: Build tests and visual checks slice

Goal

- Add unit tests for pagination and highlighting, plus a simple Playwright visual script for the search flow addressing PRD §10 Acceptance.

Scope (single PR)

- Files to touch: `apps/search/tests/test_search.py`, optional `blog_site/scripts/visual_check.py` equivalent under `travelmathlite/scripts/`, and screenshot output folder.
- Behavior: Test pagination invariants (query preserved), highlight safety with escaping, and template rendering of canonical link. Add a headless script to capture a results page screenshot for regression.
- Non-goals: Performance/load testing.

Standards

- Commits: conventional style (test/docs/chore).
- Use Django TestCase for HTTP and helper tests; Playwright for headless visual check if configured.

Acceptance

- Tests cover: pagination query preservation, highlight escaping, canonical link in head.
- Visual check script produces at least one screenshot under `travelmathlite/screenshots/search/`.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Write Django tests for `SearchView` pagination and `highlight` safety handling."
- "Add a small script to navigate to `/search/?q=ABC` and save a screenshot; document how to run with `uvx`."
- "Document results in `docs/ux/search-and-urls.md` and link test evidence."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §10 Acceptance
Requirements: FR-F-008-1, NF-003
