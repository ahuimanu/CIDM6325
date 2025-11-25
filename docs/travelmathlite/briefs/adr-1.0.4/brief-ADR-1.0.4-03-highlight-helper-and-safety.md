# BRIEF: Build highlight helper and safety slice

Goal

- Implement safe query-match highlighting in search results addressing PRD §4 F-008 and NF-003.

Scope (single PR)

- Files to touch: `apps/search/templatetags/search_extras.py` (or utility), `apps/search/templates/search/results.html`.
- Behavior: Wrap case-insensitive matches of `q` in `<mark>` while preserving HTML escaping; avoid double-escaping and XSS risks.
- Non-goals: pagination wiring (separate), URL canonicalization (separate).

Standards

- Commits: conventional style (feat/test/docs).
- Autoescape must remain enabled; implement highlighting that cooperates with Django's escaping (e.g., via `mark_safe` only on controlled markup and after escaping text segments).
- Tests: Django TestCase for helper behavior with edge cases (mixed case, multiple matches, HTML in source strings).

Acceptance

- User flow: Results show `<mark>` around exact substring matches of `q` ignoring case.
- Invariant: Highlighting does not break HTML escaping (INV-2 from ADR).
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create a template filter `highlight(text, q)` that returns safe HTML with `<mark>` around matches; ensure base text is escaped and only the `<mark>` wrapper is marked safe."
- "Add unit tests for `highlight` covering HTML injection attempts and overlapping matches."
- "Update the results template to use the filter for name/code fields."

---
ADR: adr-1.0.4-search-strategy-and-url-design.md
PRD: §4 F-008; §7 NF-003
Requirements: FR-F-008-1, NF-003
