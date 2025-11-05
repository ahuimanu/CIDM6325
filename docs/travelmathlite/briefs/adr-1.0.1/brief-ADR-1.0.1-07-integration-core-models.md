# BRIEF: Build integration with core models slice

Goal
- Integrate normalized airport and city data with core project models (PRD §1.0.1).

Scope (single PR)
- Files to touch: model integration scripts, ADR notes, test cases.
- Non-goals: dataset selection, ingestion, mapping, update automation.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.
- Django TestCase for integration logic.

Acceptance
- Core models updated and integrated with normalized data.
- Integration logic documented and tested.
- Docs updated.
- Migration included if models change.

Prompts for Copilot
- "Integrate airport/city data with core models."
- "Document integration logic and test coverage."
- "Propose commit messages for integration scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
