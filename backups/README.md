# TravelMathLite Backup Scripts

This directory contains automated backup and restore scripts for TravelMathLite airport and city data.

## Scripts

### `backup_airports.sh`

Creates timestamped backups of:
- SQLite database (`db.sqlite3`)
- Airport data (JSON fixture)
- Country and City data (JSON fixture)

Automatically cleans up backups older than 7 days.

**Usage**:
```bash
./backups/backup_airports.sh
```

**Output**:
- `backups/db.sqlite3.YYYYMMDD_HHMMSS`
- `backups/airports_YYYYMMDD_HHMMSS.json`
- `backups/base_YYYYMMDD_HHMMSS.json`

### `restore_airports.sh`

Restores database from a timestamped backup.

**Usage**:
```bash
# List available backups
./backups/restore_airports.sh

# Restore specific backup
./backups/restore_airports.sh 20251114_120000
```

**Safety Features**:
- Confirmation prompt before restore
- Creates safety backup of current database
- Runs migrations after restore
- Verifies data counts

## Best Practices

### When to Backup

Always backup before:
- Running `import_airports` command
- Rolling back migrations
- Making bulk data changes
- Testing risky operations
- Deploying to production

### Example Workflow

```bash
# 1. Create backup before risky operation
./backups/backup_airports.sh

# 2. Perform operation
uv run python travelmathlite/manage.py import_airports

# 3. Verify success
uv run python travelmathlite/manage.py validate_airports

# 4. If something went wrong, restore
./backups/restore_airports.sh 20251114_120000
```

### Backup Retention

- **Automatic**: Scripts keep last 7 days of backups
- **Manual**: Keep important backups outside `backups/` directory
- **Production**: Use additional offsite backup strategy

## Manual Backup Methods

### Django Fixtures

```bash
# Backup specific app
uv run python manage.py dumpdata airports --indent 2 > my_backup.json

# Restore
uv run python manage.py loaddata my_backup.json
```

### SQLite Database

```bash
# Backup
cp travelmathlite/db.sqlite3 my_backup.db

# Restore
cp my_backup.db travelmathlite/db.sqlite3
```

## Troubleshooting

### Script Permission Denied

```bash
chmod +x backups/backup_airports.sh
chmod +x backups/restore_airports.sh
```

### Backup Takes Too Long

Large datasets may take several minutes. Consider:
- Running during off-peak hours
- Using database-specific tools (pg_dump for PostgreSQL)
- Compressing backups with `gzip`

### Restore Fails

Check:
- Backup file exists and is not corrupted
- Database file permissions
- Sufficient disk space
- No running server holding database lock

## Related Documentation

- [Rollback and Recovery Procedures](../rollback-and-recovery.md)
- [Data Model Integration](../data-model-integration.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

**Last Updated**: 2025-11-14  
**Version**: 1.0
