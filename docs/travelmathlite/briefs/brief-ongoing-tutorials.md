# BRIEF: Ongoing Tutorials for Each ADR

Goal

- After each ADR is completed, produce a comprehensive, step-by-step tutorial (Markdown) that teaches the slice by embedding relevant excerpts from Matt Layman's "Understand Django" and official docs (Django, Bootstrap, HTMX) alongside implementation steps derived from the briefs.

Scope (recurring per-ADR)

- Files to touch: `docs/travelmathlite_tutorials/adr-<id>/tutorial-ADR-<id>-<slug>.md`.
- Inputs: ADR text, related briefs in `docs/travelmathlite/briefs/adr-<id>/`, and documentation sources.
- Non-goals: Re-implement the feature; focus on explaining, teaching, and guiding with embedded context from authoritative sources.

Standards

- Commits: conventional style (docs).
- Embed relevant excerpts or summaries from Django docs, Matt Layman chapters, Bootstrap components, and HTMX patterns directly in the tutorial to provide context without requiring readers to jump between sources.
- Structure tutorials step-by-step following the sequence in briefs: each brief becomes a tutorial section with embedded documentation context, code snippets, and verification steps.
- Keep prose clear and instructional; avoid unnecessary brevity—aim for completeness and learning over terseness.

Acceptance

- A Markdown tutorial exists per ADR under `docs/travelmathlite_tutorials/adr-<id>/`.
- Tutorial includes embedded excerpts or key concepts from Django docs, Matt Layman's chapters, Bootstrap components, and HTMX patterns relevant to each step.
- Tutorial follows brief sequence: each brief maps to a tutorial section with:
  - Brief context and goal
  - Step-by-step implementation guidance
  - Embedded documentation references (inline summaries or quoted excerpts)
  - Code snippets mirroring what was implemented
  - Verification steps (tests/URLs/expected output)
- Tutorial references: ADR, briefs, and inline documentation context.
- Include migration? no
- Update docs & PR checklist.

Deliverables (per ADR)

- [ ] `docs/travelmathlite_tutorials/adr-<id>/tutorial-ADR-<id>-<slug>.md`
  - [ ] Goals and context (link ADR + briefs)
  - [ ] Prereqs (env, dataset, settings)
  - [ ] Step-by-step sections derived from each brief in sequence:
    - [ ] Brief context and objective
    - [ ] Embedded documentation context (Django/Layman/Bootstrap/HTMX)
    - [ ] Implementation steps with code snippets
    - [ ] Verification steps (tests/URLs/output)
  - [ ] Summary and next steps
  - [ ] Full references section (Django/Layman/Bootstrap/HTMX links)

Prompts for Copilot

- "Generate a comprehensive tutorial Markdown for ADR-ADRID by reading docs/travelmathlite/adr/ (the ADR file for ADRID) and all briefs in docs/travelmathlite/briefs/ADRDIR/. Structure the tutorial following the brief sequence: for each brief, create a section that includes the brief's goal, embedded relevant excerpts from Django docs and Matt Layman's 'Understand Django', step-by-step implementation guidance with code snippets, and verification steps. Embed documentation context inline so readers don't need to jump to external sources."
- "For each section, include: (1) Brief context, (2) Relevant Django/Layman/Bootstrap/HTMX concepts (embedded as summaries or excerpts), (3) Step-by-step implementation with copy-pasteable commands and code, (4) How to Verify (tests/URLs/expected output). Keep the tone instructional and complete—optimize for learning, not brevity."

Summary

- Status: Ongoing — run after each ADR merge.
- Files: `docs/travelmathlite_tutorials/adr-<id>/*.md`.
- Tests: N/A (docs).
- Issue: optional per ADR.

---
Resources

- [Understand Django (Matt Layman)](https://www.mattlayman.com/understand-django/)
- [Django documentation](https://docs.djangoproject.com/)
- [Bootstrap documentation](https://getbootstrap.com/docs/)
- [HTMX documentation](https://htmx.org/docs/)
