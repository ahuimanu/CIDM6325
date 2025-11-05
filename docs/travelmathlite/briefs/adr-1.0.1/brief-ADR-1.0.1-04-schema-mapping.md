# BRIEF: Build schema mapping and normalization slice

Goal
- Map and normalize selected datasets to the project’s core airport and city models (PRD §1.0.1).

Scope (single PR)
- Files to touch: mapping scripts, model definitions, ADR notes.
- Non-goals: dataset selection, ingestion, validation.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.
- Django TestCase for mapping logic.

Acceptance
- Mapping logic implemented and documented.
- Sample normalized data loaded.
- Docs updated.
- Migration included if models change.

Prompts for Copilot
- "Generate schema mapping for airport/city datasets."
- "Normalize fields and document mapping logic."
- "Propose commit messages for mapping scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
