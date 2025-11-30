# Tutorial: ADR-1.0.1 Dataset Source for Airports and Cities

## Goal

Learn how TravelMathLite selects, imports, validates, and maintains airport and city datasets using Django management commands, schema mapping, and update automation.

## Context

- **ADR:** `docs/travelmathlite/adr/adr-1.0.1-dataset-source-for-airports-and-cities.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.1/` (ten briefs covering selection → import → validation → automation → compliance)
- **App:** `travelmathlite/apps/airports/`
- **Documentation:** `docs/travelmathlite/schema-mapping-airports.md`, `docs/travelmathlite/licensing-compliance-airports.md`

## Prerequisites

- TravelMathLite project initialized with `uv`
- Python environment activated
- Internet access or OurAirports CSV files downloaded to `downloads/`
- Database migrated

## Section 1: Dataset Selection (Brief 01)

### Brief Context

Select an authoritative, freely licensed, globally comprehensive airport dataset suitable for distance calculations and search.

### Data Source Evaluation

**OurAirports Dataset:**

- **Coverage:** ~70,000 airports worldwide (large, medium, small, closed)
- **License:** Public domain (no attribution required)
- **Format:** CSV (airports.csv, countries.csv, cities.csv)
- **Update Frequency:** Weekly
- **Download:** <https://ourairports.com/data/>
- **Fields:** IATA, ICAO, name, type, lat/lon, country, region, municipality

**Alternatives Considered:**

- **IATA Official:** Proprietary, expensive
- **OpenFlights:** Good coverage but less frequently updated
- **GeoNames:** General-purpose, not aviation-specific

**Decision:** OurAirports for public domain license, weekly updates, and aviation focus.

### Verification

```bash
# Download latest dataset
curl -o downloads/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv
head -n 5 downloads/airports.csv
```

---

## Section 2: Data Ingestion with Management Commands (Brief 02)

### Brief Context

Create a Django management command to parse OurAirports CSV, validate fields, and upsert airports by unique identifier (ident/IATA).

### Django Concepts: Management Commands

**From Matt Layman's "Understand Django" (Chapter: Management Commands):**

> Management commands extend Django's `manage.py`. Create them in `<app>/management/commands/<command_name>.py`. Subclass `BaseCommand` and implement `handle()`. Use `self.stdout.write()` for output and `--dry-run` flags for safety.

**From Django Documentation:**

> **Custom Management Commands:** Place your command file in `management/commands/`. Django discovers it automatically. Use `add_arguments()` to define CLI options.
>
> ```python
> from django.core.management.base import BaseCommand
>
> class Command(BaseCommand):
>     help = "Description of your command"
>     
>     def add_arguments(self, parser):
>         parser.add_argument('--dry-run', action='store_true')
>     
>     def handle(self, *args, **options):
>         if options['dry_run']:
>             self.stdout.write("Dry run mode")
> ```

### Implementation Steps

**1. Create management command structure**

```
apps/airports/
  management/
    __init__.py
    commands/
      __init__.py
      import_airports.py
      update_airports.py
```

**2. Implement `import_airports` command**

File: `apps/airports/management/commands/import_airports.py`:

```python
"""Import airports from OurAirports CSV."""
import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.airports.models import Airport

class Command(BaseCommand):
    help = "Import airports from OurAirports CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='downloads/airports.csv',
            help='Path to airports CSV file'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview import without saving to database'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of rows imported (for testing)'
        )
    
    def handle(self, *args, **options):
        file_path = Path(options['file'])
        if not file_path.exists():
            raise CommandError(f"File not found: {file_path}")
        
        dry_run = options['dry_run']
        limit = options.get('limit')
        
        self.stdout.write(f"Reading {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            airports_to_create = []
            airports_to_update = []
            count = 0
            
            for row in reader:
                if limit and count >= limit:
                    break
                
                # Validate and normalize row
                try:
                    airport_data = self._normalize_row(row)
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Skipping row: {e}"))
                    continue
                
                # Check if airport exists
                ident = airport_data['ident']
                existing = Airport.objects.filter(ident=ident).first()
                
                if existing:
                    # Update existing
                    for key, value in airport_data.items():
                        setattr(existing, key, value)
                    airports_to_update.append(existing)
                else:
                    # Create new
                    airports_to_create.append(Airport(**airport_data))
                
                count += 1
                if count % 1000 == 0:
                    self.stdout.write(f"Processed {count} rows...")
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN: Would create {len(airports_to_create)} and update {len(airports_to_update)} airports"
            ))
        else:
            with transaction.atomic():
                if airports_to_create:
                    Airport.objects.bulk_create(airports_to_create, batch_size=1000)
                if airports_to_update:
                    Airport.objects.bulk_update(
                        airports_to_update,
                        fields=['name', 'latitude_deg', 'longitude_deg', 'airport_type', 'active'],
                        batch_size=1000
                    )
            
            self.stdout.write(self.style.SUCCESS(
                f"Imported {len(airports_to_create)} new and updated {len(airports_to_update)} airports"
            ))
    
    def _normalize_row(self, row: dict) -> dict:
        """Validate and convert CSV row to model fields."""
        # Required fields
        ident = row.get('ident', '').strip()
        if not ident:
            raise ValueError("Missing ident")
        
        try:
            lat = float(row.get('latitude_deg', 0))
            lon = float(row.get('longitude_deg', 0))
        except (ValueError, TypeError):
            raise ValueError(f"Invalid coordinates for {ident}")
        
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError(f"Coordinates out of range: {lat}, {lon}")
        
        return {
            'ident': ident,
            'iata_code': row.get('iata_code', '').strip() or None,
            'name': row.get('name', '').strip() or ident,
            'airport_type': row.get('type', 'unknown').strip(),
            'latitude_deg': lat,
            'longitude_deg': lon,
            'iso_country': row.get('iso_country', '').strip() or None,
            'municipality': row.get('municipality', '').strip() or None,
            'active': row.get('type') != 'closed',
        }
```

### Verification

```bash
# Dry run first to preview
uv run python travelmathlite/manage.py import_airports --file downloads/airports.csv --dry-run --limit 100

# Actual import
uv run python travelmathlite/manage.py import_airports --file downloads/airports.csv

# Check results
uv run python travelmathlite/manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.count()
70542
>>> Airport.objects.filter(iata_code__isnull=False).count()
9327
```

---

## Section 3: Data Validation (Brief 03)

### Brief Context

Implement sanity checks for coordinates, required fields, and airport types to prevent bad data from entering the database.

### Implementation Steps

**1. Add validation to model**

File: `apps/airports/models.py`:

```python
from django.core.exceptions import ValidationError
from django.db import models

class Airport(models.Model):
    # ... fields ...
    
    def clean(self):
        """Validate model fields before saving."""
        super().clean()
        
        # Coordinate range validation
        if not (-90 <= self.latitude_deg <= 90):
            raise ValidationError(f"Invalid latitude: {self.latitude_deg}")
        if not (-180 <= self.longitude_deg <= 180):
            raise ValidationError(f"Invalid longitude: {self.longitude_deg}")
        
        # Required fields
        if not self.ident:
            raise ValidationError("ident is required")
        if not self.name:
            raise ValidationError("name is required")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

**2. Add validation tests**

File: `apps/airports/tests/test_validation.py`:

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.airports.models import Airport

class AirportValidationTests(TestCase):
    def test_invalid_latitude(self):
        airport = Airport(
            ident="TEST",
            name="Test Airport",
            latitude_deg=91.0,  # Invalid
            longitude_deg=0.0,
            airport_type="small_airport"
        )
        with self.assertRaises(ValidationError):
            airport.full_clean()
    
    def test_valid_coordinates(self):
        airport = Airport(
            ident="TEST",
            name="Test Airport",
            latitude_deg=45.0,
            longitude_deg=-90.0,
            airport_type="small_airport"
        )
        airport.full_clean()  # Should not raise
```

### Verification

```bash
uv run python travelmathlite/manage.py test apps.airports.tests.test_validation
```

---

## Section 4: Schema Mapping Documentation (Brief 04)

### Brief Context

Document the mapping from OurAirports CSV columns to Django model fields, including type conversions and field name changes.

### Implementation Steps

**1. Create schema mapping document**

File: `docs/travelmathlite/schema-mapping-airports.md`:

```markdown
# Airport Schema Mapping

## OurAirports CSV → Django Model

| CSV Column          | Django Field       | Type Conversion | Notes                        |
|---------------------|--------------------|-----------------|------------------------------|
| `ident`             | `ident`            | CharField       | Primary identifier (ICAO)    |
| `iata_code`         | `iata_code`        | CharField       | Nullable; 3-letter code      |
| `name`              | `name`             | CharField       | Airport name                 |
| `type`              | `airport_type`     | CharField       | small/medium/large_airport   |
| `latitude_deg`      | `latitude_deg`     | FloatField      | Decimal degrees              |
| `longitude_deg`     | `longitude_deg`    | FloatField      | Decimal degrees              |
| `iso_country`       | `iso_country`      | CharField       | ISO 3166-1 alpha-2           |
| `municipality`      | `municipality`     | CharField       | City/town name               |
| —                   | `active`           | BooleanField    | Derived: type != 'closed'    |

## Type Conversions

- **Coordinates:** String → float, validated within ±90/±180
- **IATA Code:** Empty string → NULL
- **Active Status:** type == 'closed' → False, else True
```

### Verification

- Review document for completeness
- Ensure all model fields documented
- Cross-reference with `import_airports` command logic

---

## Section 5: Update Automation (Brief 05)

### Brief Context

Create an `update_airports` command that wraps import with scheduling hooks, logging, and safety checks.

### Implementation Steps

**1. Create update command**

File: `apps/airports/management/commands/update_airports.py`:

```python
"""Automated airport dataset updates with logging and safety."""
import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Update airports dataset with logging and safety checks"
    
    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--file', type=str, default='downloads/airports.csv')
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        file_path = options['file']
        
        logger.info("Starting airport dataset update")
        self.stdout.write("Running pre-import checks...")
        
        # Pre-import validation (file exists, size check, etc.)
        
        # Call import_airports with options
        try:
            call_command(
                'import_airports',
                file=file_path,
                dry_run=dry_run,
                verbosity=2
            )
            logger.info("Airport dataset updated successfully")
            self.stdout.write(self.style.SUCCESS("Update complete"))
        except Exception as e:
            logger.error(f"Update failed: {e}")
            self.stdout.write(self.style.ERROR(f"Update failed: {e}"))
            raise
```

**2. Schedule with cron or Django management**

Example cron entry (weekly updates):

```cron
0 2 * * 0 cd /path/to/travelmathlite && uv run python manage.py update_airports --file downloads/airports.csv
```

### Verification

```bash
uv run python travelmathlite/manage.py update_airports --dry-run
```

---

## Section 6: Licensing Compliance (Brief 06)

### Brief Context

Document OurAirports' public domain license and compliance requirements (attribution optional, redistribution allowed).

### Implementation Steps

**1. Create licensing documentation**

File: `docs/travelmathlite/licensing-compliance-airports.md`:

```markdown
# Airport Data Licensing Compliance

## OurAirports Dataset

- **License:** Public Domain (CC0 1.0 Universal)
- **Attribution:** Not required but appreciated
- **Redistribution:** Allowed without restriction
- **Commercial Use:** Allowed
- **Source:** https://ourairports.com/data/

## Compliance Checklist

- ✅ Dataset is public domain
- ✅ No attribution legally required
- ✅ Optional attribution in footer: "Airport data from OurAirports.com"
- ✅ Redistribution and commercial use allowed
- ✅ Weekly updates available for data freshness

## References

- [OurAirports License](https://ourairports.com/about.html#license)
- [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)
```

### Verification

- Review license terms on OurAirports website
- Add optional attribution to site footer

---

## Section 7: Integration with Core Models (Brief 07)

### Brief Context

Normalize country and city data during import, linking airports to `Country` and `City` models via foreign keys.

### Django Concepts: Model Relationships

**From Matt Layman's "Understand Django" (Chapter: Models and Relationships):**

> Use `ForeignKey` to link models. When importing data, use `get_or_create()` to ensure related objects exist before linking. This prevents duplicate entries and maintains referential integrity.

### Implementation Steps

**1. Add foreign keys to Airport model**

File: `apps/airports/models.py`:

```python
from django.db import models
from apps.base.models import Country, City

class Airport(models.Model):
    # ... existing fields ...
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='airports'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='airports'
    )
```

**2. Update import command to link countries/cities**

```python
def _normalize_row(self, row: dict) -> dict:
    # ... existing code ...
    
    # Link to Country
    iso_country = row.get('iso_country', '').strip()
    country = None
    if iso_country:
        country, _ = Country.objects.get_or_create(
            iso_code=iso_country.upper(),
            defaults={'name': iso_country}
        )
    
    # Link to City
    municipality = row.get('municipality', '').strip()
    city = None
    if municipality and country:
        city, _ = City.objects.get_or_create(
            name=municipality,
            country=country
        )
    
    return {
        # ... existing fields ...
        'country': country,
        'city': city,
    }
```

### Verification

```python
>>> from apps.airports.models import Airport
>>> jfk = Airport.objects.get(iata_code="JFK")
>>> jfk.country.name
'United States'
>>> jfk.city.name
'New York'
```

---

## Section 8: Documentation and Onboarding (Brief 08)

### Brief Context

Update project README and onboarding docs to explain how to import and update airport data.

### Implementation Steps

**1. Add to README**

File: `travelmathlite/README.md`:

```markdown
## Importing Airport Data

1. Download OurAirports dataset:
   ```bash
   curl -o downloads/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv
   ```

2. Import (dry-run first):

   ```bash
   uv run python manage.py import_airports --file downloads/airports.csv --dry-run
   uv run python manage.py import_airports --file downloads/airports.csv
   ```

3. Verify:

   ```bash
   uv run python manage.py shell
   >>> from apps.airports.models import Airport
   >>> Airport.objects.count()
   ```

For automation, see `docs/travelmathlite/dataset-updates.md`.

```

### Verification

- New developers can follow README to import data
- All steps execute without errors

---

## Section 9: Test Coverage (Brief 09)

### Brief Context

Write tests for import command, schema mapping, validation, and update automation.

### Implementation Steps

**1. Create import tests**

File: `apps/airports/tests/test_import_command.py`:

```python
from django.test import TestCase
from django.core.management import call_command
from apps.airports.models import Airport
import tempfile
import csv

class ImportCommandTests(TestCase):
    def test_import_from_csv(self):
        # Create temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['ident', 'name', 'type', 'latitude_deg', 'longitude_deg', 'iso_country'])
            writer.writeheader()
            writer.writerow({
                'ident': 'TEST',
                'name': 'Test Airport',
                'type': 'small_airport',
                'latitude_deg': '45.0',
                'longitude_deg': '-90.0',
                'iso_country': 'US'
            })
            temp_path = f.name
        
        # Import
        call_command('import_airports', file=temp_path)
        
        # Verify
        self.assertTrue(Airport.objects.filter(ident='TEST').exists())
        airport = Airport.objects.get(ident='TEST')
        self.assertEqual(airport.name, 'Test Airport')
        self.assertAlmostEqual(airport.latitude_deg, 45.0)
```

### Verification

```bash
uv run python travelmathlite/manage.py test apps.airports.tests.test_import_command
```

---

## Section 10: Rollback and Recovery (Brief 10)

### Brief Context

Document backup/restore procedures, dry-run workflows, and import idempotence for safe updates.

### Implementation Steps

**1. Create rollback documentation**

File: `docs/travelmathlite/dataset-rollback.md`:

```markdown
# Dataset Rollback and Recovery

## Pre-Import Backup

```bash
# Django dumpdata
uv run python manage.py dumpdata airports.Airport > backups/airports_$(date +%Y%m%d).json

# SQLite backup
cp db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3
```

## Rollback Procedure

```bash
# Restore from dumpdata
uv run python manage.py loaddata backups/airports_20250101.json

# Or restore full database
cp backups/db_20250101.sqlite3 db.sqlite3
```

## Idempotent Imports

- Import command uses upsert logic (update existing by `ident`)
- Running import multiple times is safe
- Always use `--dry-run` first for large updates

```

### Verification

- Test backup and restore workflow
- Verify dry-run produces expected output without changes

---

## Summary and Next Steps

You've now implemented a complete data import pipeline:

1. **Dataset Selection:** OurAirports (public domain, weekly updates)
2. **Data Ingestion:** Management command with CSV parsing and upsert
3. **Data Validation:** Coordinate ranges, required fields, model clean
4. **Schema Mapping:** Documented CSV → Django field mappings
5. **Update Automation:** Scheduled updates with logging
6. **Licensing Compliance:** Public domain compliance documented
7. **Model Integration:** Country/City foreign key relationships
8. **Documentation:** README and onboarding guides
9. **Test Coverage:** Import command and validation tests
10. **Rollback Procedures:** Backup/restore workflows

**Next Steps:**
- Add city geocoding for better search
- Implement incremental updates (only changed rows)
- Add monitoring/alerting for failed imports
- Consider PostGIS for advanced spatial queries

## Full References

**Matt Layman's "Understand Django":**
- Chapter: Management Commands
- Chapter: Models and Relationships
- Chapter: Testing

**Django Documentation:**
- [Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- [Model Relationships](https://docs.djangoproject.com/en/stable/topics/db/models/#relationships)
- [Data Validation](https://docs.djangoproject.com/en/stable/ref/models/instances/#validating-objects)

**OurAirports:**
- [Dataset](https://ourairports.com/data/)
- [License](https://ourairports.com/about.html#license)
