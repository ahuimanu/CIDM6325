# BRIEF: Build dataset selection slice

Goal
- Implement dataset selection for airports and cities addressing PRD §1.0.1.

Scope (single PR)
- Files to touch: docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md, supporting notes or scripts.
- Non-goals: data ingestion, validation, or transformation.

Standards
- Commits: conventional style (feat/docs/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance
- User flow: Document candidate datasets, pros/cons, and licensing.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot
- "List and compare open datasets for airports and cities."
- "Summarize licensing and update recommendations."
- "Propose commit messages for dataset selection."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
