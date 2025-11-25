# BRIEF: Build templates and navbar search field slice

Goal

- Integrate a navbar search input and consistent results template hierarchy addressing PRD §4 F-007.

Scope (single PR)

- Files to touch: `apps/base/templates/base.html` (or common layout), `apps/search/templates/search/results.html`, navbar partial include, optional form snippet.
- Behavior: Display a search input in the navbar that submits to `/search/` with `q`; ensure focus/placeholder UX and preserve `q` value in the input on results pages.
- Non-goals: Data filtering logic (separate), highlight implementation (separate).

Standards

- Commits: conventional style (feat/docs/style).
- Use template inheritance; keep markup minimal and accessible; no inline scripts.

Acceptance

- User flow: User can submit a query from the navbar on any page and lands on `/search/?q=...` with the input pre-filled.
- Base layout remains consistent; no regressions in other app templates.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add a navbar search form that directs to the namespaced `search` URL with GET and preserves value."
- "Create or update `search/results.html` extending the base layout and slotting in pagination and highlight hooks."
- "Add a minimal integration test that submits from a non-search page and asserts redirect to results with `q`."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §4 F-007; §10 Acceptance
Requirements: FR-F-007-1
