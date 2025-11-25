# Airport Fixtures

This directory contains JSON fixtures for airport data that can be loaded into the database for testing and initial deployment.

## Usage

### Load fixture into database

```bash
cd travelmathlite
uv run python manage.py loaddata apps/airports/fixtures/airports.json
```

### Create a new fixture

```bash
# Export all airports
uv run python manage.py export_airports

# Export only airports with IATA codes
uv run python manage.py export_airports --filter-iata

# Export limited set for testing
uv run python manage.py export_airports --limit 100

# Custom output path
uv run python manage.py export_airports --output path/to/fixture.json
```

## Fixture Contents

- **airports.json**: Sample airport data for development and testing
- Includes core fields: ident, iata_code, name, coordinates, country, etc.
- Can be regenerated from live data using `export_airports` command

## Deployment Workflow

1. On source machine: Export production data
   ```bash
   uv run python manage.py export_airports --filter-iata --output production_airports.json
   ```

2. On target machine: Load fixture after migrations
   ```bash
   uv run python manage.py migrate
   uv run python manage.py loaddata production_airports.json
   ```

## Notes

- Fixtures are version-controlled for reproducibility
- Large fixtures (>1000 records) should be compressed or stored externally
- Use `--filter-iata` to keep fixture size manageable
- Fixtures preserve primary keys for referential integrity
