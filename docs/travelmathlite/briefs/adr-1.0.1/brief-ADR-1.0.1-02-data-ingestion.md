# BRIEF: Build data ingestion slice

Goal
- Implement data ingestion for airports and cities datasets addressing PRD §1.0.1.

Scope (single PR)
- Files to touch: ETL scripts, Django management commands, docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md.
- Non-goals: dataset selection, validation logic.

Standards
- Commits: conventional style (feat/docs/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance
- User flow: Download, clean, transform, and load selected datasets into the database.
- SSL certificate issues resolved for HTTPS downloads.
- Fixture export/import commands available for deployment rehydration.
- Include migration? yes
- Update docs & PR checklist.

Deliverables (Completed)
- ✅ `import_airports` management command with --dry-run, --file, --url, --filter-iata, --limit
- ✅ `export_airports` management command for creating JSON fixtures
- ✅ Airport model with proper indexes
- ✅ Migration for Airport table
- ✅ Fixture directory with README and sample data
- ✅ SSL-safe download implementation
- ✅ Idempotent upsert logic tested and verified

Prompts for Copilot
- "Generate ETL pipeline for airport/city datasets."
- "Create Django management command for ingestion with SSL support."
- "Add fixture export command for deployment rehydration."
- "Propose commit messages for ingestion scripts."

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
Issue: #31
