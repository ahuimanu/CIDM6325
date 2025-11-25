# TravelMathLite Documentation Index

Comprehensive documentation for the TravelMathLite project.

## Getting Started

### For New Contributors

1. **[Contributing Guide](CONTRIBUTING.md)** 🌟 *Start here!*
   - Quick start and setup
   - Dataset workflow overview
   - Code standards and conventions
   - Troubleshooting common issues

2. **[Django Project Setup with uv](django-project-setup-with-uv.md)**
   - Initial project setup
   - Using uv for package management
   - Environment configuration

3. **[Dataset Workflow Quick Reference](dataset-workflow-quickref.md)** 📋
   - Command cheat sheet
   - Common tasks
   - Troubleshooting tips

## Dataset and Data Management

### Import and Integration

1. **[Data Model Integration Guide](data-model-integration.md)** 🔧
   - Import workflow details
   - Country/City FK linking
   - Query helpers and usage
   - Validation and monitoring
   - Troubleshooting quick reference

2. **[Schema Mapping Reference](schema-mapping-airports.md)** 📊
   - OurAirports CSV field mapping
   - Model field descriptions
   - Type conversions and normalization
   - Example mappings

3. **[Update Automation](update-automation-airports.md)** ⏰
   - Scheduled updates with cron
   - Django-crontab integration
   - Celery Beat configuration
   - Monitoring and alerting

### Operations and Disaster Recovery

1. **[Rollback and Recovery Procedures](rollback-and-recovery.md)** 🛡️ *Important!*
   - Migration rollback procedures
   - Database backup and restore workflows
   - FK detachment and re-linking
   - Import failure recovery
   - Automated backup/restore scripts
   - Emergency procedures

### Legal and Compliance

1. **[Licensing and Compliance](licensing-compliance-airports.md)** ⚖️
   - Dataset license (Public Domain)
   - Attribution requirements
   - Compliance checklist
   - Risk management

## Architecture

### Architecture Decision Records (ADRs)

ADRs document significant architectural choices and their rationale.

- **[ADR-1.0.1: Dataset Source](adr/adr-1.0.1-dataset-source-for-airports-and-cities.md)**
  - Selection of OurAirports dataset
  - License and field coverage analysis
  - Import approach decisions

- **[ADR Template](adr/adr_template_v1.0.1.md)**
  - Template for new ADRs

### Product Requirements

- **[Product Requirements Document (PRD)](prd/)**
  - Project scope and features
  - Functional and non-functional requirements
  - Success metrics

## Implementation Guides

### Briefs

Task-level implementation guides organized by ADR:

- **[ADR-1.0.1 Briefs](briefs/adr-1.0.1/)**
  - Brief-ADR-1.0.1-01: Licensing compliance
  - Brief-ADR-1.0.1-02: Schema mapping
  - Brief-ADR-1.0.1-03: Airport model
  - Brief-ADR-1.0.1-04: Import command
  - Brief-ADR-1.0.1-05: Validation command
  - Brief-ADR-1.0.1-06: Update automation
  - Brief-ADR-1.0.1-07: Core model integration
  - Brief-ADR-1.0.1-08: Documentation and onboarding *(current)*

- **[Brief Template](briefs/copilot_brief_template_v1.0.0.md)**
  - Template for new task briefs

### Calculators & Algorithms

- **[Distance, Time, and Cost Algorithms](algorithms/distance-and-cost.md)** — Formulas, defaults, examples, and limitations for distance/time/cost calculations

## Reference Materials

### Datasets

- **[datasets/](datasets/)** - Sample data and reference files

### GitHub Workflows

- **[GitHub CLI Commands](briefs/adr-1.0.1/gh-commands-adr-1.0.1.md)**
  - Issue creation scripts
  - PR workflow automation

## Quick Links by Task

### I want to

- **Get started as a new contributor** → [Contributing Guide](CONTRIBUTING.md)
- **Import airport data** → [Data Model Integration](data-model-integration.md)
- **Look up a command** → [Quick Reference](dataset-workflow-quickref.md)
- **Understand field mappings** → [Schema Mapping](schema-mapping-airports.md)
- **Schedule automatic updates** → [Update Automation](update-automation-airports.md)
- **Check license compliance** → [Licensing](licensing-compliance-airports.md)
- **Understand an architectural decision** → [ADRs](adr/)
- **Implement a feature** → [Briefs](briefs/)
- **See project requirements** → [PRD](prd/)

## Documentation Standards

### Writing Guidelines

- Use Markdown format
- Include code examples where appropriate
- Link related documents
- Keep language clear and concise
- Update the index when adding new docs

### File Organization

```text
docs/travelmathlite/
├── README.md                           # This index
├── CONTRIBUTING.md                     # Contributor onboarding
├── dataset-workflow-quickref.md       # Command cheat sheet
├── data-model-integration.md          # Import workflow
├── schema-mapping-airports.md         # Field mapping
├── update-automation-airports.md      # Scheduling
├── licensing-compliance-airports.md   # Legal compliance
├── django-project-setup-with-uv.md   # Setup guide
├── algorithms/                       # Calculation methods & formulas
├── adr/                               # Architecture decisions
├── briefs/                            # Task implementation guides
├── prd/                               # Requirements
└── datasets/                          # Reference data
```

## Contributing to Documentation

### Adding New Documentation

1. Create the document in the appropriate location
2. Follow existing formatting conventions
3. Add entry to this index
4. Link from related documents
5. Submit PR with conventional commit

Example commit:

```text
docs: add troubleshooting guide for import errors

- Common import failures and solutions
- Debug command examples
- Link from CONTRIBUTING.md

Refs #XX
```

### Updating Existing Documentation

1. Make changes maintaining existing structure
2. Update "Last Updated" date if present
3. Note changes in PR description
4. Test all command examples

## External Resources

### Django Documentation

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

### Dataset Sources

- [OurAirports](https://ourairports.com/data/)
- [OurAirports GitHub](https://github.com/davidmegginson/ourairports-data)

### Tools

- [uv Package Manager](https://docs.astral.sh/uv/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Playwright Testing](https://playwright.dev/python/)

## Support and Questions

- **In-project**: Check related documents above
- **Issues**: GitHub Issues for bugs/features
- **Discussions**: Class CIDM 6325 forums
- **Architecture**: Review ADRs for context

---

### Tutorials

- **ADR-1.0.0: Application Architecture & App Boundaries** — [Tutorial](../travelmathlite_tutorials/adr-1.0.0/tutorial-ADR-1.0.0-application-architecture-and-app-boundaries.md)
- **ADR-1.0.1: Dataset Source for Airports and Cities** — [Tutorial](../travelmathlite_tutorials/adr-1.0.1/tutorial-ADR-1.0.1-dataset-source-for-airports-and-cities.md)
- **ADR-1.0.2: Distance & Cost Calculators** — [Tutorial](../travelmathlite_tutorials/adr-1.0.2/tutorial-ADR-1.0.2-distance-and-cost.md)
- **ADR-1.0.3: Nearest Airport Lookup** — [Tutorial](../travelmathlite_tutorials/adr-1.0.3/tutorial-ADR-1.0.3-nearest-airport.md)

Ongoing process brief: [brief-ongoing-tutorials.md](briefs/brief-ongoing-tutorials.md)

**Last Updated:** 2025-11-14
