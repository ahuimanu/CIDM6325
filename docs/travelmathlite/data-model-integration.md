# Core Data Integration Guide

This guide explains how OurAirports records are linked to the normalized `Country` and `City` models introduced by ADR-1.0.16. Use it before running imports, during QA, and when troubleshooting linkage coverage.

---

## 1. Models and migrations

- `apps/base/models.py` defines `Country` and `City` with timestamp mixins, slug/search helpers, and admin registrations (`apps/base/admin.py`).
- Migrations: `base/0001_initial.py` seeds the tables; `airports/0002_airport_core_integrations.py` adds FK fields plus the `active` flag to `Airport`.
- Admin tips:
  - Country admin exposes search by ISO/name and an `active` filter.
  - City admin filters by country, shows timezone/population, and is safe for inline CSV exports.

## 2. Import workflow

| Step | Responsible file | Notes |
|------|------------------|-------|
| Parse CSV row | `apps/airports/schema_mapping.py` (`normalize_csv_row`) | Produces Python-typed dict with `active`, placeholder `country`/`city` keys |
| Link Country/City | `apps/airports/services/integration.py` | Loads optional `downloads/countries.csv`, caches lookups, exposes `link_location()` |
| Upsert airport | `apps/airports/management/commands/import_airports.py` | Passes FK objects + `active` flag into `Airport.objects.update_or_create()` |
| Stats/metrics | `import_airports` summary | Prints total created/updated rows plus `Country links` / `City links` counts and creation totals |

**Command flags**

```bash
# Standard import (downloads CSV, links Country/City)
uv run python travelmathlite/manage.py import_airports

# Debug linking behaviour without writing FK rows
uv run python travelmathlite/manage.py import_airports --skip-country-link --skip-city-link

# Run from local CSV but keep linking enabled
uv run python travelmathlite/manage.py import_airports --file downloads/airports.csv

# Dry-run skip writes entirely (link metrics suppressed)
uv run python travelmathlite/manage.py import_airports --dry-run
```

## 3. Query helpers and usage

- `Airport.objects.active()` – quick filter for non-closed airports.
- `Airport.objects.search(term)` – case-insensitive search that spans name/codes/municipality/country.
- `Airport.objects.nearest(lat, lon, limit=3, iso_country=None, unit="km"|"mi")` – bounding-box pre-filter plus haversine ordering; always attaches `distance_km` per result and, when `unit="mi"`, also attaches `distance_mi`.
- Use these in calculators/search views instead of hand-crafted filters so Country/City joins remain consistent.

## 4. Validation and monitoring

- `uv run python travelmathlite/manage.py validate_airports` prints existing quality checks plus two new sections:
  - **Normalized Country links** – warns when FK coverage is lower than 100%.
  - **Normalized City links** – warns when airports with municipalities lack FK rows.
- CI recommendation: run `python travelmathlite/manage.py test apps.base apps.airports` after schema changes; this suite includes importer linking tests and QuerySet assertions.

## 5. Troubleshooting and rollback

| Symptom | Checks | Mitigation |
|---------|--------|------------|
| Country coverage stays near 0% | Ensure `iso_country` column populated; confirm `Country` records exist (maybe remove `--skip-country-link`). | Seed `downloads/countries.csv` or clear caches by restarting `import_airports`. |
| City coverage low | Many rows have blank `municipality` values. Inspect warnings via `--verbose`. | Accept blank coverage or seed fallback cities manually via admin. |
| Import fails on slug uniqueness | Conflicting normalized city names. | Merge/rename City rows via admin; rerun import (idempotent). |
| Need to revert | Use Django migrations to roll back `airports/0002` and `base/0001`, then remove FK fields from import command. | Only revert if class requirements change; otherwise keep migrations applied. |

Always run imports/validation via `uv run` to ensure the correct virtual environment is active. For more architectural context see ADR-1.0.1 and ADR-1.0.16.

**For comprehensive rollback procedures**, see **[Rollback and Recovery](rollback-and-recovery.md)** which includes:
- Migration rollback procedures
- Database backup and restore workflows
- FK detachment procedures
- Import failure recovery
- Automated backup/restore scripts

## Related Documentation

- **[Quick Reference](dataset-workflow-quickref.md)** - Command cheat sheet
- **[Contributing Guide](CONTRIBUTING.md)** - Onboarding for new contributors
- **[Schema Mapping](schema-mapping-airports.md)** - Field mapping details
- **[Update Automation](update-automation-airports.md)** - Scheduling imports
- **[Licensing](licensing-compliance-airports.md)** - Dataset license and attribution
- **[Rollback and Recovery](rollback-and-recovery.md)** - 🛡️ Disaster recovery procedures
