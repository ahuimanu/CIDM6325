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

## Deliverables (Completed)

1. **Update Automation Command**
   - File: `apps/airports/management/commands/update_airports.py`
   - Features:
     - Wraps `import_airports` with timing and reporting
     - Transaction-safe updates (rollback on error, commit on success)
     - Dry-run mode for testing (`--dry-run`)
     - Filter by IATA codes (`--filter-iata`)
     - Custom data source URL (`--url`)
     - Force download (`--force`)
     - Initial/final count tracking with net change calculation
     - Duration timing (start, end, elapsed)
     - Summary reporting with clear status messages
     - Error handling with logging to Python logging system
   - Usage:
     ```bash
     python manage.py update_airports
     python manage.py update_airports --dry-run
     python manage.py update_airports --filter-iata
     ```

2. **Comprehensive Test Suite**
   - File: `apps/airports/tests_update_command.py`
   - 10 tests covering:
     - Command invocation and argument passing
     - Dry-run mode behavior (no database changes)
     - Filter options (IATA, custom URL)
     - Count tracking (initial, final, net change)
     - Duration timing
     - Summary reporting
     - Error handling and exception logging
     - stdout/stderr pass-through to import command
     - Integration test with real OurAirports download
   - All tests passing (verified 2025-11-14)

3. **Documentation**
   - File: `docs/travelmathlite/update-automation-airports.md`
   - Sections:
     - Command usage and options
     - Scheduling strategies (cron, django-crontab, Celery Beat)
     - Update frequency recommendations
     - Idempotent update behavior
     - Logging and monitoring
     - Error handling and common issues
     - Backup and rollback procedures
     - Performance considerations
     - Security and compliance
     - Troubleshooting guide

4. **ADR Update**
   - File: `docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md`
   - Added section: "Update automation and sync strategy"
   - Documents:
     - Update automation command capabilities
     - Scheduling strategies and frequency recommendations
     - Error handling and monitoring approach
     - Idempotent update behavior
     - Performance characteristics (70K airports in ~2-3 minutes)
     - Backup and rollback procedures
     - Security and compliance considerations
     - Test coverage (10 tests)

5. **Key Features Implemented**
   - **Transaction Safety**: Database rollback on any error
   - **Idempotent Updates**: `update_or_create()` ensures safe re-execution
   - **Error Handling**: All exceptions caught, logged, and reported
   - **Monitoring**: Clear output with counts, timing, and error summaries
   - **Testing**: Dry-run mode for safe update testing
   - **Scheduling**: Documented strategies for cron, django-crontab, Celery Beat
   - **Performance**: Optimized for large datasets (70K airports)
   - **Logging**: Integration with Python logging system

6. **Issue Management**
   - Issue #37 created: "Brief 05: Implement update automation for airport data"
   - Link: https://github.com/ahuimanu/CIDM6325/issues/37
   - Status: Ready for closure after commit

---
ADR: adr-1.0.1-dataset-source-for-airports-and-cities.md
PRD: §1.0.1
Issue: #37
