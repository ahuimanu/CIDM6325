# BRIEF: Build test coverage for data integrity slice

Goal
- Ensure test coverage for data integrity of airports and cities datasets (PRD §1.0.1).

Scope (single PR)
- Files to touch: test scripts, ADR notes, CI configs.
- Non-goals: ingestion, mapping, update automation, integration.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.
- Django TestCase for all tests.

Acceptance
- Automated tests for data integrity and validation rules.
- CI updated to include data tests.
- Docs updated.
- No migration unless schema changes.

Prompts for Copilot
- "Create Django TestCase for airport/city data integrity."
- "Integrate data tests into CI workflow."
- "Propose commit messages for test coverage."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
