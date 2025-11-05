# BRIEF: Build rollback and recovery procedures slice

Goal
- Implement rollback and recovery procedures for airports and cities dataset operations (PRD §1.0.1).

Scope (single PR)
- Files to touch: recovery scripts, ADR notes, documentation.
- Non-goals: ingestion, mapping, update automation, integration.

Standards
- Conventional commits; PEP 8; docstrings; type hints.
- No secrets; env via settings.

Acceptance
- Documented rollback and recovery steps for dataset operations.
- Scripts or manual procedures included.
- Docs updated.
- No migration unless schema changes.

Prompts for Copilot
- "Draft rollback and recovery procedures for dataset operations."
- "Document recovery steps and risks."
- "Propose commit messages for rollback scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
