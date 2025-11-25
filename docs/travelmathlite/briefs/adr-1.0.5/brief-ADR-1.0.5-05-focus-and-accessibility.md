# BRIEF: Build focus management and accessibility enhancements slice

Goal

- Add focus management and ARIA attributes for HTMX updates addressing PRD §7 NF-002.

Scope (single PR)

- Files to touch: Partial templates, calculator form templates, optional HTMX configuration in base template.
- Behavior: Add `hx-swap` with `focus-scroll:true` or manual focus management; include ARIA live regions for result announcements; ensure keyboard navigation works after HTMX swaps.
- Non-goals: New calculator features, validation logic changes.

Standards

- Commits: conventional style (feat/docs).
- Follow WCAG 2.1 AA guidelines for focus and announcements.
- Test with keyboard-only navigation and screen reader (manual verification).

Acceptance

- User flow: After HTMX form submission, focus moves to result region or error summary; screen readers announce updates.
- ARIA live regions (e.g., `aria-live="polite"`) present for dynamic result updates.
- Keyboard navigation works correctly after swap.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Add `aria-live='polite'` to result containers in partial templates for screen reader announcements."
- "Configure HTMX swap with focus options: `hx-swap='outerHTML focus-scroll:true'` or add `tabindex='-1'` to result container and use `hx-on::after-swap` for manual focus."
- "Document accessibility approach in `docs/ux/htmx-patterns.md` with keyboard and screen reader testing notes."

---
ADR: adr-1.0.5-forms-and-htmx-progressive-enhancement.md
PRD: §7 NF-002
Requirements: NF-002 (Accessibility)
