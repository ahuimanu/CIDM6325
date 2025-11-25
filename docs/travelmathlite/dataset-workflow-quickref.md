# Dataset Workflow Quick Reference

A cheat sheet for working with airport and city data in TravelMathLite.

## Common Commands

| Task | Command |
|------|---------|
| **Import/update airports** | `uv run python manage.py import_airports` |
| **Import from local file** | `uv run python manage.py import_airports --file downloads/airports.csv` |
| **Dry-run preview** | `uv run python manage.py import_airports --dry-run` |
| **Skip linking (debug)** | `uv run python manage.py import_airports --skip-country-link --skip-city-link` |
| **Validate data quality** | `uv run python manage.py validate_airports` |
| **Scheduled update** | `uv run python manage.py update_airports` |
| **Run tests** | `uv run python manage.py test apps.base apps.airports` |
| **Start dev server** | `uv run python manage.py runserver` |

## Import Workflow

```
Download CSV → Parse & Normalize → Link Country/City → Upsert Airport → Report Stats
```

### 1. Download CSV
- Source: https://davidmegginson.github.io/ourairports-data/airports.csv
- Auto-downloaded by `import_airports` command
- Or download manually to `downloads/airports.csv`

### 2. Parse & Normalize
- File: `apps/airports/schema_mapping.py`
- Converts CSV strings to Python types
- Maps `type` → `airport_type`, derives `active` flag
- Validates lat/lon ranges, elevation values

### 3. Link Country/City
- File: `apps/airports/services/integration.py`
- Looks up/creates `Country` via `iso_country`
- Looks up/creates `City` via `municipality` + `iso_country`
- Caches lookups for performance

### 4. Upsert Airport
- Uses `ident` as unique key
- `update_or_create()` for idempotency
- Sets FKs to Country and City

### 5. Report Stats
- Total created/updated
- Country links count
- City links count
- Duration and row processing speed

## Key Models

### Airport (`apps/airports/models.py`)
```python
Airport(
    ident='KDEN',              # Primary key (ICAO/local code)
    iata_code='DEN',           # Optional 3-letter IATA
    name='Denver International',
    airport_type='large_airport',
    latitude_deg=39.8561,
    longitude_deg=-104.6737,
    elevation_ft=5434,
    iso_country='US',
    iso_region='US-CO',
    municipality='Denver',
    country=Country(...),      # FK to normalized Country
    city=City(...),            # FK to normalized City
    active=True                # Derived: type != 'closed'
)
```

### Country (`apps/base/models.py`)
```python
Country(
    code='US',                 # Primary key (ISO 3166-1 alpha-2)
    name='United States',
    active=True
)
```

### City (`apps/base/models.py`)
```python
City(
    name='Denver',
    slug='denver',
    country=Country('US'),     # FK
    timezone='America/Denver',
    population=715522,
    active=True
)
```

## Query Helpers

```python
# Active airports only
Airport.objects.active()

# Search by name/code/location
Airport.objects.search('denver')

# Nearest airports
Airport.objects.nearest(
    lat=39.7392,
    lon=-104.9903,
    limit=5,
    iso_country='US',  # Optional filter
    unit='mi'          # 'km' or 'mi'
)
```

## Data Quality Checks

### validate_airports command reports:

1. **Basic Metrics**
   - Total airports
   - With IATA codes
   - With coordinates
   - With elevation

2. **Country Linking**
   - Total linked
   - Coverage percentage
   - Warnings if <100%

3. **City Linking**
   - Total linked
   - Coverage for airports with municipality
   - Expected lower coverage (many blank municipalities)

### Expected Coverage

- **Country**: ~100% (iso_country present in CSV)
- **City**: 50-80% (many airports lack municipality)

## Troubleshooting

### Issue: "Country not found"
**Fix**: Ensure `apps.base` migrations applied
```bash
uv run python manage.py migrate apps.base
```

### Issue: Low city coverage
**Status**: Expected behavior
**Reason**: Many airports have blank `municipality` field
**Check**: Run `validate_airports` for actual coverage

### Issue: Import slow
**Tips**:
- Use `--file` with pre-downloaded CSV
- Check network connection for remote download
- Integration service caches Country/City lookups

### Issue: uv command not found
**Fix**: Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

## Flags Reference

### import_airports flags

| Flag | Effect |
|------|--------|
| `--file PATH` | Import from local CSV instead of downloading |
| `--dry-run` | Preview without writing to database |
| `--skip-country-link` | Don't link Country FK (debug) |
| `--skip-city-link` | Don't link City FK (debug) |
| `--verbose` | Show detailed progress and warnings |
| `--filter-iata` | Only import airports with IATA codes |

### update_airports flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview without writing |
| `--url URL` | Use custom CSV source |
| `--filter-iata` | Only update airports with IATA codes |

## File Locations

```
apps/
  airports/
    models.py                    # Airport model
    schema_mapping.py            # CSV → Python normalization
    admin.py                     # Django admin config
    management/commands/
      import_airports.py         # Import command
      validate_airports.py       # Validation command
      update_airports.py         # Scheduled update command
    services/
      integration.py             # Country/City linking
  base/
    models.py                    # Country, City models
    admin.py                     # Admin config
downloads/
  airports.csv                   # Downloaded dataset (gitignored)
  countries.csv                  # Optional country seed data
docs/travelmathlite/
  data-model-integration.md      # Full workflow guide
  schema-mapping-airports.md     # Field mapping reference
  update-automation-airports.md  # Scheduling guide
```

## Integration Points

### Admin Interface
- `/admin/airports/airport/` - Browse/edit airports
- `/admin/base/country/` - Manage countries
- `/admin/base/city/` - Manage cities

### Query Methods (in views/calculators)
```python
from apps.airports.models import Airport

# Get active airports near a point
nearby = Airport.objects.nearest(39.7, -104.9, limit=3)

# Search airports
results = Airport.objects.search('international')

# Filter by country
us_airports = Airport.objects.filter(iso_country='US')
```

## Commit Message Template

```
feat: add airport import feature

- Implement OurAirports CSV parsing
- Add Country/City FK linking
- Report coverage metrics

Refs #42
```

## Next Steps

1. **New to the project?** Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Need details?** See [data-model-integration.md](data-model-integration.md)
3. **Scheduling updates?** See [update-automation-airports.md](update-automation-airports.md)
4. **Field mapping?** See [schema-mapping-airports.md](schema-mapping-airports.md)

---

**Quick help**: `uv run python manage.py <command> --help`
