# BRIEF: Build update automation and sync strategy slice

Goal
- Automate updates and syncing for airport and city datasets (PRD §1.0.1).

Scope (single PR)
- Files to touch: update scripts, cron configs, ADR notes.
- Non-goals: initial ingestion, validation, mapping.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.
- Django TestCase for update logic.

Acceptance
- Automated update process implemented and documented.
- Update logs and error handling in place.
- Docs updated.
- No migration unless schema changes.

Prompts for Copilot
- "Create update automation for airport/city datasets."
- "Document sync strategy and error handling."
- "Propose commit messages for update scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
