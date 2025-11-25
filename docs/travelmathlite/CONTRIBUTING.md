# Contributing to TravelMathLite

Welcome! This guide helps new contributors understand the dataset workflow for airports and cities data.

## Quick Start

1. **Clone and set up the project**
   ```bash
   git clone <repository-url>
   cd CIDM6325/travelmathlite
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Run migrations**
   ```bash
   uv run python manage.py migrate
   ```

4. **Import airport data**
   ```bash
   uv run python manage.py import_airports
   ```

## Dataset Workflow

### Overview

TravelMathLite uses the [OurAirports](https://ourairports.com/data/) dataset for airport information. The workflow includes:

1. **Import** - Download and load airport data
2. **Link** - Connect airports to normalized Country/City models
3. **Validate** - Check data quality and coverage
4. **Update** - Periodically refresh from upstream

### Key Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `import_airports` | Load/update airport data | `uv run python manage.py import_airports` |
| `validate_airports` | Check data quality | `uv run python manage.py validate_airports` |
| `update_airports` | Scheduled updates with logging | `uv run python manage.py update_airports` |

### Import Workflow Details

The import process handles three main tasks:

1. **Parse CSV** - Read and normalize OurAirports CSV format
   - File: `apps/airports/schema_mapping.py`
   - Converts types, validates ranges
   - Maps CSV columns to model fields

2. **Link Locations** - Connect to normalized Country/City
   - File: `apps/airports/services/integration.py`
   - Uses ISO country codes and municipality names
   - Caches lookups for performance

3. **Upsert Records** - Create or update Airport models
   - File: `apps/airports/management/commands/import_airports.py`
   - Idempotent (safe to run multiple times)
   - Reports created/updated counts

### Common Tasks

#### Import from downloaded file

```bash
# Download CSV first
curl -o downloads/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv

# Import from local file
uv run python manage.py import_airports --file downloads/airports.csv
```

#### Dry-run to preview changes

```bash
uv run python manage.py import_airports --dry-run
```

#### Import without linking (debug mode)

```bash
uv run python manage.py import_airports --skip-country-link --skip-city-link
```

#### Check data quality

```bash
uv run python manage.py validate_airports
```

## Architecture Decisions

Key architectural decisions are documented in ADRs (Architecture Decision Records):

- **[ADR-1.0.1](adr/adr-1.0.1-dataset-source-for-airports-and-cities.md)** - Dataset source selection (OurAirports)
- **[ADR-1.0.3](adr/)** - Schema mapping and model design
- **[ADR-1.0.16](adr/)** - Normalized Country/City integration

## Code Standards

- **Language**: Python 3.12 + Django
- **Style**: PEP 8; docstrings on public functions; type hints on new code
- **Testing**: Django TestCase (not pytest)
- **Tools**: `uv` for package management; Ruff for linting/formatting

### Before Submitting

1. **Lint and format**
   ```bash
   uvx ruff check .
   uvx ruff format .
   ```

2. **Run tests**
   ```bash
   uv run python manage.py test apps.base apps.airports
   ```

3. **Validate imports**
   ```bash
   uv run python manage.py validate_airports
   ```

## Commit Conventions

Use conventional commits with issue references:

```
feat: add city linking to airport import

- Integrate apps.base.City model
- Add municipality-based lookup
- Report linkage coverage in import stats

Refs #42
```

Keywords:
- `Refs #<issue>` - Ongoing work
- `Closes #<issue>` - Final commit when merging

## Pull Request Guidelines

- Keep PRs small (<300 lines changed)
- Include migration plan and rollback notes
- Use Copilot PR summary to brief reviewers
- Link related issues and ADRs

**For detailed rollback procedures**, see **[Rollback and Recovery](rollback-and-recovery.md)**.

## Documentation

Key documentation files:

- **[data-model-integration.md](data-model-integration.md)** - Import workflow and troubleshooting
- **[schema-mapping-airports.md](schema-mapping-airports.md)** - Field mapping reference
- **[update-automation-airports.md](update-automation-airports.md)** - Scheduling automated updates
- **[licensing-compliance-airports.md](licensing-compliance-airports.md)** - License and attribution
- **[rollback-and-recovery.md](rollback-and-recovery.md)** - 🛡️ Disaster recovery and backup procedures

## Getting Help

1. Check existing documentation in `docs/travelmathlite/`
2. Review ADRs for architectural context
3. Search closed issues for similar problems
4. Ask in project discussions or class forums

## Troubleshooting

### Import fails with "Country not found"

**Cause**: Missing Country records in database.

**Solution**:
```bash
# Ensure base migrations are applied
uv run python manage.py migrate apps.base

# Optionally seed countries CSV
# (integration service will auto-create from iso_country codes)
```

### Low city linkage coverage

**Cause**: Many airports have blank `municipality` fields.

**Solution**: This is expected. The validation command will report coverage. You can manually add City records via admin if needed.

### Command not found: uv

**Cause**: `uv` not installed or not in PATH.

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

### Data corruption or import failures

**See**: **[Rollback and Recovery](rollback-and-recovery.md)** for comprehensive procedures including:
- Database backup and restore
- Migration rollback
- Import failure recovery
- FK detachment procedures
- Automated backup/restore scripts

## Dataset Updates

The OurAirports dataset is updated regularly by community contributors. To keep data fresh:

1. **Manual updates**: Run `import_airports` command
2. **Scheduled updates**: Use `update_airports` with cron/Celery (see update-automation-airports.md)
3. **Validation**: Always validate after updates

## Next Steps

After getting set up:

1. Read the [PRD](prd/travelmathlite_prd_v1.0.0.md) to understand project goals
2. Review [ADR-1.0.1](adr/adr-1.0.1-dataset-source-for-airports-and-cities.md) for dataset rationale
3. Explore the admin interface: `uv run python manage.py runserver`
4. Try the nearest airport calculator (when search features are implemented)

## Questions?

- Project documentation: `docs/travelmathlite/`
- Architecture decisions: `docs/travelmathlite/adr/`
- Task briefs: `docs/travelmathlite/briefs/`

Happy contributing!
