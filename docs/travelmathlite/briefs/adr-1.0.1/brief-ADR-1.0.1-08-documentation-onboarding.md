# BRIEF: Build documentation and onboarding slice

Goal
- Document the dataset workflow and onboard contributors for airports and cities data (PRD §1.0.1).

Scope (single PR)
- Files to touch: onboarding docs, ADR notes, workflow guides.
- Non-goals: ingestion, mapping, update automation, integration.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.

Acceptance
- Contributor documentation updated for dataset workflow.
- Onboarding guide created and linked in README.
- Docs updated.
- No migration.

Prompts for Copilot
- "Draft onboarding docs for dataset workflow."
- "Summarize steps for new contributors."
- "Propose commit messages for documentation updates."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
