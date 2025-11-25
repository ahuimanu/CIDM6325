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

Deliverables (Completed)
- ✅ Schema mapping module with type definitions (`schema_mapping.py`)
- ✅ `normalize_csv_row()` function with full type conversions
- ✅ Field mapping documentation (10 mapped, 8 unmapped fields)
- ✅ Comprehensive documentation (`docs/travelmathlite/schema-mapping-airports.md`)
- ✅ 17 schema mapping tests (complete/minimal rows, conversions, validation, integration)
- ✅ All tests passing (44 total airport tests)
- ✅ ADR updated with schema mapping section
- ✅ No migration needed (model already supports mapping)

Prompts for Copilot
- "Generate schema mapping for airport/city datasets."
- "Normalize fields and document mapping logic."
- "Propose commit messages for mapping scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
