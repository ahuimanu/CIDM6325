# Airport Data Update Automation

This document describes the automated update strategy for airport data in TravelMathLite.

## Overview

The `update_airports` management command provides automated synchronization with the OurAirports dataset. It wraps the `import_airports` command with additional logging, error handling, and reporting suitable for scheduled execution.

## Command Usage

### Basic Update

```bash
# Update airport data from default source
python manage.py update_airports
```

### Dry Run

```bash
# Preview what would be updated without making changes
python manage.py update_airports --dry-run
```

### With Filters

```bash
# Only update airports with IATA codes
python manage.py update_airports --filter-iata
```

### Custom Source

```bash
# Use a different CSV URL
python manage.py update_airports --url https://example.com/airports.csv
```

## Scheduling Updates

### Using Cron (Linux/macOS)

Add to crontab (`crontab -e`):

```cron
# Update airport data daily at 2:00 AM
0 2 * * * cd /path/to/travelmathlite && /path/to/python manage.py update_airports >> /var/log/airport_updates.log 2>&1

# Update weekly on Sunday at 3:00 AM
0 3 * * 0 cd /path/to/travelmathlite && /path/to/python manage.py update_airports >> /var/log/airport_updates.log 2>&1
```

### Using Django-Crontab

1. Install django-crontab:
   ```bash
   pip install django-crontab
   ```

2. Add to `settings.py`:
   ```python
   INSTALLED_APPS = [
       # ...
       'django_crontab',
   ]

   CRONJOBS = [
       ('0 2 * * *', 'django.core.management.call_command', ['update_airports']),
   ]
   ```

3. Add cron jobs:
   ```bash
   python manage.py crontab add
   ```

### Using Celery Beat

1. Create a Celery task in `apps/airports/tasks.py`:
   ```python
   from celery import shared_task
   from django.core.management import call_command

   @shared_task
   def update_airport_data():
       call_command('update_airports')
   ```

2. Configure beat schedule in `settings.py`:
   ```python
   from celery.schedules import crontab

   CELERY_BEAT_SCHEDULE = {
       'update-airports-daily': {
           'task': 'apps.airports.tasks.update_airport_data',
           'schedule': crontab(hour=2, minute=0),
       },
   }
   ```

## Update Strategy

### Idempotent Updates

The update process is idempotent using `update_or_create()`:

- **Existing airports**: Updated with latest data
- **New airports**: Created in database
- **Removed airports**: Remain in database (no deletions)

### Data Integrity

1. **Transaction Safety**: Updates run in a database transaction
2. **Validation**: All data validated before saving
3. **Error Handling**: Exceptions logged; database unchanged on failure
4. **Dry Run**: Preview mode for testing update logic

### Update Frequency Recommendations

| Data Type | Recommended Frequency | Rationale |
|-----------|----------------------|-----------|
| Airport data | Weekly | OurAirports updates frequently, but airport changes are infrequent |
| IATA codes only | Daily | More stable subset, suitable for production |
| Development | On-demand | Manual updates as needed |

## Logging

### Command Output

The update command provides detailed output:

```
============================================================
Airport Data Update
============================================================
Started: 2025-11-14 02:00:00

Current airports in database: 10245

Fetching latest data from OurAirports...

=== Import Summary ===
Total rows: 67891
Created: 156
Updated: 10245
Skipped: 57490
Errors: 0

============================================================
Update Summary
============================================================
Initial count: 10245
Final count: 10401
Net change: +156

Completed: 2025-11-14 02:02:15
Duration: 135.24 seconds

✓ Airport data updated successfully!
```

### Python Logging

The command logs to Python's logging system:

```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/travelmathlite/airport_updates.log',
        },
    },
    'loggers': {
        'apps.airports.management.commands.update_airports': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Error Handling

### Common Issues

1. **Network Errors**
   - Download failures are caught and logged
   - Database remains unchanged
   - Retry on next scheduled run

2. **Data Validation Errors**
   - Invalid rows are skipped with warnings
   - Valid data still imported
   - Error count reported in summary

3. **Database Errors**
   - Transaction rolled back
   - Error logged with full traceback
   - No partial updates

### Monitoring

Monitor these metrics:

- **Success rate**: Percentage of successful updates
- **Duration**: Update execution time
- **Net change**: Number of records added/updated
- **Error count**: Failed row imports

### Alerting

Set up alerts for:

- Failed updates (exit code ≠ 0)
- Excessive duration (> 10 minutes)
- High error rate (> 1% of rows)
- No net change for > 30 days (potential data staleness)

## Testing Updates

### Dry Run Testing

```bash
# Test update without making changes
python manage.py update_airports --dry-run

# Test with custom data source
python manage.py update_airports --dry-run --url file:///tmp/test_airports.csv
```

### Automated Tests

Run the test suite:

```bash
python manage.py test apps.airports.tests_update_command
```

## Backup Strategy

### Pre-Update Backups

For production environments, consider pre-update backups:

```bash
#!/bin/bash
# Script: backup_and_update_airports.sh

# Backup database
pg_dump mydb > /backups/airports_$(date +%Y%m%d_%H%M%S).sql

# Run update
python manage.py update_airports

# Check exit code
if [ $? -eq 0 ]; then
    echo "Update successful"
else
    echo "Update failed - restore from backup if needed"
    exit 1
fi
```

### Rollback Procedure

If an update causes issues:

1. **Stop the application**
2. **Restore from backup**:
   ```bash
   psql mydb < /backups/airports_20251114_020000.sql
   ```
3. **Investigate the issue** in development
4. **Re-enable updates** after fix

## Performance Considerations

### Large Datasets

For large datasets (> 100K airports):

- **Bulk operations**: Uses `update_or_create()` which is optimized
- **Transaction size**: Single transaction, but fast due to bulk operations
- **Memory usage**: Processes row-by-row, minimal memory footprint
- **Duration**: Expect ~2-3 minutes for 70K airports

### Optimization Tips

1. **Filter by IATA**: Use `--filter-iata` to update only relevant airports
2. **Off-peak scheduling**: Run during low-traffic hours
3. **Read replicas**: Use read replicas for queries during updates
4. **Indexes**: Ensure `ident` index exists for fast lookups

## Security

### Access Control

- **Command execution**: Requires server access
- **Data source**: HTTPS by default
- **Credentials**: No API keys needed (public dataset)

### Data Validation

- **Coordinate ranges**: Validated before save
- **Required fields**: Enforced by model
- **SQL injection**: Protected by Django ORM

## Compliance

### Data Attribution

OurAirports data is public domain, but attribution is appreciated:

> Airport data sourced from OurAirports (https://ourairports.com/data/)

### License

- **OurAirports data**: Public Domain
- **Update automation**: Part of TravelMathLite (project license)

## Troubleshooting

### Update Hangs

```bash
# Check for long-running queries
SELECT pid, query, state, query_start 
FROM pg_stat_activity 
WHERE query LIKE '%airports%';
```

### Disk Space

```bash
# Check available space
df -h /var/lib/postgresql

# Clean old backups
find /backups -name "airports_*.sql" -mtime +30 -delete
```

### Network Issues

```bash
# Test connectivity
curl -I https://davidmegginson.github.io/ourairports-data/airports.csv

# Use local file if network unavailable
python manage.py update_airports --url file:///tmp/airports.csv
```

## References

- ADR-1.0.1: Dataset source for airports and cities
- `import_airports` command: Base import functionality
- `validate_airports` command: Data validation
- OurAirports documentation: https://ourairports.com/help/
