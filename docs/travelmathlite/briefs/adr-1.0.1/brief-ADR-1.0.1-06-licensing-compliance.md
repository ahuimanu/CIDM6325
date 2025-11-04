# BRIEF: Build licensing and compliance review slice

Goal
- Review licensing and compliance for selected airport and city datasets (PRD §1.0.1).

Scope (single PR)
- Files to touch: compliance notes, ADR documentation.
- Non-goals: ingestion, mapping, update automation.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.

Acceptance
- Licensing and compliance notes documented for all datasets.
- Risks and obligations summarized.
- Docs updated.
- No migration.

Prompts for Copilot
- "Summarize licensing and compliance for selected datasets."
- "Document obligations and risks."
- "Propose commit messages for compliance review."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
