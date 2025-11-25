# BRIEF: Build forms and validation slice

Goal

- Implement Django forms for distance and cost calculators with validation and defaults addressing PRD §4 F-001, F-003.

Scope (single PR)

- Files to touch: `apps/calculators/forms.py`, unit tests for forms.
- Non-goals: Views, templates, HTMX integration.

Standards

- Commits: conventional style (feat/fix/docs/refactor/test/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).
- Use Django forms best practices; ModelForm where applicable.

Acceptance

- User flow: Forms accept city names, airport codes, or lat/long coordinates; validate and normalize to coordinates.
- Forms provide defaults from settings (route factor, fuel economy, etc.) but allow user overrides.
- Unit selection (km/miles) via form field.
- Include migration? no (forms only)
- Update docs & PR checklist.

Deliverables (Completed)

- [x] `calculators/forms.py` with forms:
  - `DistanceCalculatorForm`: fields for origin/destination (text or lat/long), unit selection (km/miles), route factor override
  - `CostCalculatorForm`: inherits or includes distance fields, adds fuel economy, fuel price, unit preferences
- [x] Validation logic:
  - Accept city names and resolve to coordinates (via airports model lookup or hardcoded city list)
  - Accept airport IATA codes and resolve to coordinates
  - Accept direct lat/long input (e.g., "40.7128,-74.0060")
  - Validate numeric ranges (lat: -90 to 90, lon: -180 to 180)
- [x] Populate defaults from Django settings
- [x] Unit tests:
  - Valid city/airport/coordinate inputs
  - Invalid inputs (bad coords, unknown city)
  - Default value population
  - Clean methods normalize inputs to coordinate pairs

Prompts for Copilot

- "Generate Django forms in `calculators/forms.py` for distance and cost calculators. DistanceCalculatorForm should have fields: origin (CharField), destination (CharField), unit (ChoiceField for km/miles), route_factor (FloatField with default from settings.ROUTE_FACTOR). CostCalculatorForm should extend this with fuel_economy and fuel_price fields."
- "Implement clean methods that normalize origin/destination to lat/long coordinates. Support: city names (lookup from airports model or hardcoded list), IATA airport codes (lookup from airports model), direct lat/long as comma-separated string."
- "Add validation for lat/long ranges and numeric field constraints. Raise ValidationError with helpful messages."
- "Create Django TestCase for form validation: test valid inputs (city, airport, coords), test invalid inputs, test default value population."
- "Propose commit messages for forms and validation implementation."

Summary

- Status: Completed — forms for distance and cost with validation and defaults.
- Files: `apps/calculators/forms.py`, `apps/calculators/tests.py`.
- Tests: 39 tests passing at completion for this slice.
- Commit: [83860bd](https://github.com/ahuimanu/CIDM6325/commit/83860bd).
- Issue: #47.

---
ADR: adr-1.0.2-geo-calculation-methods.md
PRD: §4 F-001, F-003, FR-F-001-2
Issue: #47
