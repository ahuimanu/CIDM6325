# BRIEF: ADR-1.0.0 — Documentation: app layout guide

Goal

- Document the project app layout and namespacing decisions to reduce drift and onboard students.

Scope (single PR)

- Create `docs/architecture/app-layout.md` describing `apps/*`, template structure, and URL namespacing.
- Add a section to README with a short summary and link to the doc.
- Non-goals: deep design docs beyond layout.

Standards

- Keep examples minimal and accurate; update if paths change.

Acceptance

- `docs/architecture/app-layout.md` exists and shows tree snippets and reverse() examples.
- README has a short "App layout" section with the link.

Prompts for Copilot

- "Draft an app-layout doc with a tree listing of apps, where templates live, and example reverse() calls."
- "Propose a concise README paragraph that links to the app-layout doc."

Traceability

- ADR: ADR-1.0.0 (§Documentation updates).
- PRD: §4 Scope.
