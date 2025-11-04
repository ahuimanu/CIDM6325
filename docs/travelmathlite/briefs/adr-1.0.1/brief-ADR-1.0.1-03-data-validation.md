# BRIEF: Build data validation slice

Goal
- Implement data validation for ingested airports and cities datasets addressing PRD §1.0.1.

Scope (single PR)
- Files to touch: validation scripts, Django TestCase, docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md.
- Non-goals: dataset selection, ingestion pipeline.

Standards
- Commits: conventional style (feat/test/docs/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance
- User flow: Validate required fields, coordinate ranges, uniqueness, and report anomalies.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot
- "Generate validation logic for airport/city data."
- "Create Django TestCase for validation rules."
- "Propose commit messages for validation scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
