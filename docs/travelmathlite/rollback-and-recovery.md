# Rollback and Recovery Procedures

This document provides comprehensive rollback and recovery procedures for TravelMathLite dataset operations, focusing on airport and city data management.

## Overview

TravelMathLite uses Django migrations and idempotent import commands to manage airport and city data. This guide covers:

- Rollback procedures for imports and migrations
- Recovery from failed operations
- Database backup and restore workflows
- FK relationship management during rollback
- Common failure scenarios and mitigation

## Quick Reference

| Scenario | Command/Action | Risk Level |
|----------|---------------|------------|
| Undo last import | `python manage.py rollback_airports` | Low |
| Rollback migration | `python manage.py migrate <app> <migration>` | Medium |
| Restore from backup | `python manage.py loaddata <fixture>` | Medium |
| Detach City FKs | Admin bulk action or script | Low |
| Full database restore | Database-specific restore command | High |

## Import Rollback Procedures

### Scenario 1: Rollback Recent Import

**When**: Just imported airports.csv and need to undo changes.

**Risk**: Low - Import is idempotent, can re-run safely.

**Procedure**:

```bash
# Option A: Delete all airports (nuclear option)
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.all().delete()
>>> exit()

# Option B: Use custom rollback command (if implemented)
uv run python manage.py rollback_airports --since="2025-11-14 10:00:00"

# Option C: Restore from backup (see Database Restore section)
```

**Verification**:
```bash
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.count()
0  # Or expected count before import
```

### Scenario 2: Rollback Partial/Failed Import

**When**: Import command failed mid-execution or imported corrupt data.

**Risk**: Low - Database transaction rolled back automatically on error.

**Django automatically rolls back transactions on error**. However, if data was committed:

```bash
# Check what was imported
uv run python manage.py validate_airports

# If needed, delete recent imports by date
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> from django.utils import timezone
>>> cutoff = timezone.now() - timezone.timedelta(hours=1)
>>> recent = Airport.objects.filter(created_at__gte=cutoff)
>>> print(f"Found {recent.count()} recent airports")
>>> recent.delete()  # Only if you're sure
```

### Scenario 3: Rollback Import with Bad FK Links

**When**: Airports linked to wrong Country/City records.

**Risk**: Low - FKs can be safely cleared and re-linked.

**Procedure**:

```bash
# Option A: Clear all FK links, then re-import with linking
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.update(country=None, city=None)
>>> exit()

# Re-import with fresh linking
uv run python manage.py import_airports

# Option B: Delete and re-import specific country
>>> from apps.airports.models import Airport
>>> Airport.objects.filter(iso_country='XX').delete()
# Then re-import just that country's airports
```

## Migration Rollback Procedures

### Check Migration Status

```bash
# See current migration state
uv run python manage.py showmigrations

# See migration history for specific app
uv run python manage.py showmigrations airports
uv run python manage.py showmigrations base
```

### Rollback Airport Migrations

**Risk**: Medium - Data loss if not backed up first.

**Current migrations**:
- `airports/0001_initial.py` - Initial Airport model
- `airports/0002_airport_core_integrations.py` - Adds country, city FKs + active flag

**Rollback to before core integrations**:

```bash
# BACKUP FIRST (see Database Backup section)

# Rollback to 0001 (removes country, city, active fields)
uv run python manage.py migrate airports 0001

# Rollback completely (removes Airport model)
uv run python manage.py migrate airports zero
```

**⚠️ Warning**: Rolling back `0002` removes `country`, `city`, and `active` fields permanently.

**Recovery**:
```bash
# Re-apply migrations
uv run python manage.py migrate airports

# Re-import data
uv run python manage.py import_airports
```

### Rollback Base (Country/City) Migrations

**Risk**: HIGH - Country/City used by Airport FKs.

**Current migrations**:
- `base/0001_initial.py` - Country and City models

**Rollback procedure**:

```bash
# MUST detach Airport FKs first (see FK Management section)

# Step 1: Clear Airport FK references
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.update(country=None, city=None)
>>> exit()

# Step 2: Rollback base migration
uv run python manage.py migrate base zero

# Step 3: Re-apply if needed
uv run python manage.py migrate base
```

**⚠️ Critical**: Attempting to rollback `base` without clearing FKs will fail due to PROTECT on Country FK.

## Foreign Key Management

### Understanding FK Cascade Behavior

| Model | FK Field | on_delete | Behavior |
|-------|----------|-----------|----------|
| Airport | country | PROTECT | Cannot delete Country if referenced |
| Airport | city | SET_NULL | Deleting City sets airport.city=None |

### Safe FK Detachment

**Scenario**: Need to delete Country records but airports reference them.

**Procedure**:

```bash
# Option A: Clear all country FKs
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.update(country=None)
>>> # Now safe to delete countries

# Option B: Clear specific country
>>> Airport.objects.filter(country__iso_code='US').update(country=None)
>>> from apps.base.models import Country
>>> Country.objects.get(iso_code='US').delete()

# Option C: Use admin bulk action
# In admin: select airports → Actions → "Clear country FK"
```

### Re-linking After Detachment

```bash
# Re-run import to restore FK links
uv run python manage.py import_airports

# Or use integration service directly
uv run python manage.py shell
>>> from apps.airports.services.integration import AirportLocationIntegrator
>>> integrator = AirportLocationIntegrator()
>>> 
>>> from apps.airports.models import Airport
>>> for airport in Airport.objects.filter(country=None):
>>>     location = integrator.link_location(
>>>         airport.iso_country,
>>>         airport.municipality,
>>>         airport.latitude_deg,
>>>         airport.longitude_deg
>>>     )
>>>     airport.country = location.country
>>>     airport.city = location.city
>>>     airport.save()
```

## Database Backup and Restore

### Backup Procedures

**SQLite (Development)**:

```bash
# Full database backup
cp travelmathlite/db.sqlite3 travelmathlite/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# Verify backup
ls -lh travelmathlite/db.sqlite3*
```

**Django Fixtures (Portable)**:

```bash
# Backup airports
uv run python manage.py dumpdata airports.Airport --indent 2 > backups/airports_$(date +%Y%m%d).json

# Backup countries and cities
uv run python manage.py dumpdata base.Country base.City --indent 2 > backups/base_$(date +%Y%m%d).json

# Full backup
uv run python manage.py dumpdata --indent 2 > backups/full_$(date +%Y%m%d).json

# Exclude session/contenttypes
uv run python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions --indent 2 > backups/data_$(date +%Y%m%d).json
```

**PostgreSQL (Production)**:

```bash
# Dump specific tables
pg_dump -h localhost -U user -t airports_airport -t base_country -t base_city dbname > backups/airport_data.sql

# Full database dump
pg_dump -h localhost -U user dbname > backups/full_db_$(date +%Y%m%d).sql
```

### Restore Procedures

**SQLite**:

```bash
# Stop any running server
# Replace database
cp travelmathlite/db.sqlite3.backup.20251114_120000 travelmathlite/db.sqlite3

# Verify
uv run python manage.py migrate
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.count()
```

**Django Fixtures**:

```bash
# WARNING: loaddata does NOT clear existing data first
# Option A: Clear tables manually
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.all().delete()

# Option B: Use flush (DANGER: clears ALL data)
# uv run python manage.py flush --no-input

# Load fixture
uv run python manage.py loaddata backups/airports_20251114.json

# Verify
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.count()
```

**PostgreSQL**:

```bash
# Drop and recreate database (DANGER)
dropdb dbname
createdb dbname

# Restore from dump
psql -h localhost -U user dbname < backups/full_db_20251114.sql

# Or restore specific tables
psql -h localhost -U user dbname < backups/airport_data.sql
```

## Recovery Scenarios

### Scenario 1: Import Command Hangs

**Symptoms**: `import_airports` runs indefinitely, no progress.

**Diagnosis**:
```bash
# Check process
ps aux | grep manage.py

# Check database locks (PostgreSQL)
# SELECT * FROM pg_locks WHERE NOT GRANTED;
```

**Recovery**:
```bash
# Kill the process
kill -9 <pid>

# Database transaction should auto-rollback
# Verify no partial data
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> # Check counts/data
```

### Scenario 2: Corrupted Airport Data

**Symptoms**: Invalid coordinates, missing required fields, bad FKs.

**Diagnosis**:
```bash
uv run python manage.py validate_airports
```

**Recovery**:
```bash
# Option A: Delete bad records
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> # Find and delete corrupt records
>>> bad = Airport.objects.filter(latitude_deg__gt=90)
>>> bad.delete()

# Option B: Full re-import
>>> Airport.objects.all().delete()
>>> exit()
uv run python manage.py import_airports

# Option C: Restore from backup
cp backups/db.sqlite3.backup travelmathlite/db.sqlite3
```

### Scenario 3: Missing Country/City Links

**Symptoms**: Low FK coverage, airports with NULL country/city.

**Diagnosis**:
```bash
uv run python manage.py validate_airports
# Check "Normalized Country links" and "City links" sections
```

**Recovery**:
```bash
# Re-run import to restore links
uv run python manage.py import_airports

# Or re-link manually (see FK Management section)
```

### Scenario 4: Duplicate Airports

**Symptoms**: Multiple airports with same ident (should be impossible due to PK).

**Actually**: Different ident but same IATA code.

**Recovery**:
```bash
# Find duplicates
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> from django.db.models import Count
>>> dupes = Airport.objects.values('iata_code').annotate(count=Count('ident')).filter(count__gt=1, iata_code__isnull=False)
>>> for d in dupes:
>>>     print(f"IATA {d['iata_code']}: {d['count']} airports")
>>>     Airport.objects.filter(iata_code=d['iata_code']).values('ident', 'name', 'airport_type')

# Manual resolution in admin or:
>>> # Keep only large_airport, delete others
>>> for iata in dupes:
>>>     code = iata['iata_code']
>>>     keep = Airport.objects.filter(iata_code=code, airport_type='large_airport').first()
>>>     if keep:
>>>         Airport.objects.filter(iata_code=code).exclude(ident=keep.ident).delete()
```

### Scenario 5: Migration Conflicts

**Symptoms**: `migrate` command fails with "conflicts detected".

**Recovery**:
```bash
# Check conflicts
uv run python manage.py makemigrations --check

# If conflicts exist, resolve by:
# Option A: Squash migrations
uv run python manage.py squashmigrations airports 0001 0002

# Option B: Merge migrations
uv run python manage.py makemigrations --merge

# Option C: Reset migrations (DANGER - requires data backup)
# 1. Backup data
# 2. Delete migration files (keep __init__.py)
# 3. Rollback to zero
# 4. Recreate initial migration
# 5. Restore data
```

## Automated Recovery Scripts

### Create Backup Script

```bash
# backups/backup_airports.sh
#!/bin/bash
set -e

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Backing up database..."
cp travelmathlite/db.sqlite3 $BACKUP_DIR/db.sqlite3.$DATE

echo "Backing up airports..."
uv run python travelmathlite/manage.py dumpdata airports.Airport --indent 2 > $BACKUP_DIR/airports_$DATE.json

echo "Backing up base models..."
uv run python travelmathlite/manage.py dumpdata base.Country base.City --indent 2 > $BACKUP_DIR/base_$DATE.json

echo "Backup complete: $BACKUP_DIR/*$DATE*"
ls -lh $BACKUP_DIR/*$DATE*

# Keep only last 7 days
find $BACKUP_DIR -name "*.json" -mtime +7 -delete
find $BACKUP_DIR -name "db.sqlite3.*" -mtime +7 -delete
```

Make executable:
```bash
chmod +x backups/backup_airports.sh
```

Run before risky operations:
```bash
./backups/backup_airports.sh
```

### Create Restore Script

```bash
# backups/restore_airports.sh
#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_date>"
    echo "Example: $0 20251114_120000"
    echo ""
    echo "Available backups:"
    ls -1 backups/db.sqlite3.* | sed 's/backups\/db.sqlite3.//'
    exit 1
fi

DATE=$1
BACKUP_DIR="backups"

if [ ! -f "$BACKUP_DIR/db.sqlite3.$DATE" ]; then
    echo "Error: Backup $BACKUP_DIR/db.sqlite3.$DATE not found"
    exit 1
fi

echo "⚠️  WARNING: This will replace your current database!"
read -p "Are you sure? (yes/no) " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo "Restoring database from $DATE..."
cp $BACKUP_DIR/db.sqlite3.$DATE travelmathlite/db.sqlite3

echo "Running migrations..."
uv run python travelmathlite/manage.py migrate

echo "Verifying restore..."
uv run python travelmathlite/manage.py shell -c "
from apps.airports.models import Airport
from apps.base.models import Country, City
print(f'Airports: {Airport.objects.count()}')
print(f'Countries: {Country.objects.count()}')
print(f'Cities: {City.objects.count()}')
"

echo "Restore complete!"
```

Make executable:
```bash
chmod +x backups/restore_airports.sh
```

Usage:
```bash
# List available backups
./backups/restore_airports.sh

# Restore specific backup
./backups/restore_airports.sh 20251114_120000
```

## Best Practices

### Before Risky Operations

1. **Create backup**
   ```bash
   ./backups/backup_airports.sh
   ```

2. **Test in dry-run mode** (if available)
   ```bash
   uv run python manage.py import_airports --dry-run
   ```

3. **Document the operation**
   - What you're doing
   - Why you're doing it
   - Expected outcome
   - Rollback plan

4. **Check current state**
   ```bash
   uv run python manage.py validate_airports
   ```

### During Operations

1. **Monitor progress**
   - Watch command output
   - Check logs
   - Monitor system resources

2. **Be ready to abort**
   - Keep terminal accessible
   - Know how to kill process (Ctrl+C or `kill`)

3. **Document issues**
   - Error messages
   - Data snapshots
   - Unexpected behavior

### After Operations

1. **Verify success**
   ```bash
   uv run python manage.py validate_airports
   uv run python manage.py test apps.airports apps.base
   ```

2. **Keep backup temporarily**
   - Don't delete backup immediately
   - Keep for at least 24 hours
   - Verify app works correctly

3. **Document outcome**
   - What changed
   - Any issues encountered
   - Lessons learned

## Troubleshooting Guide

### Import Fails with "IntegrityError"

**Cause**: Duplicate primary key or unique constraint violation.

**Fix**:
```bash
# Check for existing data
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.filter(ident='<problematic_ident>').delete()
```

### Cannot Delete Country

**Error**: `ProtectedError: Cannot delete Country because Airport references it`

**Fix**:
```bash
# Clear country FKs first
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.filter(country__iso_code='US').update(country=None)
>>> # Now can delete
>>> from apps.base.models import Country
>>> Country.objects.get(iso_code='US').delete()
```

### Migration Rollback Fails

**Error**: `Unapplying migration would lose data`

**Fix**:
```bash
# Backup data first
uv run python manage.py dumpdata airports > backup.json

# Force rollback
uv run python manage.py migrate airports 0001 --fake

# Or manually edit migration
# Set migration.operations = [] to skip destructive operations
```

### Restore Fails with "Duplicate Key"

**Cause**: loaddata doesn't clear existing data.

**Fix**:
```bash
# Clear tables first
uv run python manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.all().delete()

# Then load
uv run python manage.py loaddata backup.json
```

## Emergency Procedures

### Complete Database Reset

**⚠️ EXTREME DANGER**: All data lost.

```bash
# Backup first!
cp travelmathlite/db.sqlite3 travelmathlite/db.sqlite3.emergency_backup

# Delete database
rm travelmathlite/db.sqlite3

# Recreate from migrations
uv run python manage.py migrate

# Re-import fresh data
uv run python manage.py import_airports
```

### Corrupt Database Recovery

**Symptoms**: SQLite errors, database won't open.

**Recovery**:
```bash
# Try to dump what you can
sqlite3 travelmathlite/db.sqlite3 ".dump" > dump.sql

# Create new database
rm travelmathlite/db.sqlite3
uv run python manage.py migrate

# Import dump
sqlite3 travelmathlite/db.sqlite3 < dump.sql

# If that fails, restore from backup
cp backups/db.sqlite3.<latest> travelmathlite/db.sqlite3
```

## Production Considerations

### High-Availability Setup

- Use read replicas for queries
- Use write primary for imports
- Schedule imports during low-traffic windows
- Use connection pooling

### Zero-Downtime Migrations

```bash
# 1. Add new fields as nullable
# 2. Deploy code that writes to both old and new
# 3. Backfill data
# 4. Deploy code that only uses new fields
# 5. Remove old fields in next migration
```

### Backup Strategy

- **Hourly**: Incremental backups
- **Daily**: Full database backup
- **Weekly**: Offsite backup copy
- **Before imports**: Manual backup
- **Retention**: 7 daily, 4 weekly, 12 monthly

## Related Documentation

- [Data Model Integration](data-model-integration.md) - Import workflow and troubleshooting
- [Test Coverage and CI](test-coverage-and-ci.md) - Testing after rollback
- [Contributing Guide](CONTRIBUTING.md) - Development practices
- [ADR-1.0.1](adr/adr-1.0.1-dataset-source-for-airports-and-cities.md) - Architecture decisions

---

**Last Updated**: 2025-11-14  
**Version**: 1.0  
**Status**: Production Ready
