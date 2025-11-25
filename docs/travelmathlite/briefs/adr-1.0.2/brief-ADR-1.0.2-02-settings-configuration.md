# BRIEF: Build settings configuration slice

Goal

- Add configurable settings for route factor and average driving speed addressing PRD §4 F-001.

Scope (single PR)

- Files to touch: `core/settings.py`, documentation for settings.
- Non-goals: Implementation of calculation logic, form integration.

Standards

- Commits: conventional style (feat/fix/docs/refactor/test/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance

- User flow: Settings provide defaults for route factor and average speed that can be overridden via environment variables.
- Settings documented and accessible in calculators.
- Include migration? no
- Update docs & PR checklist.

Deliverables (Completed)

- [x] Add to `core/settings.py`:
  - `ROUTE_FACTOR = float(os.getenv('ROUTE_FACTOR', '1.2'))`
  - `AVG_SPEED_KMH = float(os.getenv('AVG_SPEED_KMH', '80'))`
  - `FUEL_PRICE_PER_LITER = float(os.getenv('FUEL_PRICE_PER_LITER', '1.50'))`  # Euro default
  - `FUEL_ECONOMY_L_PER_100KM = float(os.getenv('FUEL_ECONOMY_L_PER_100KM', '7.5'))`
- [x] Add comment documentation explaining each setting
- [x] Verify via tests settings load with expected defaults
- [x] Update README or settings documentation with environment variable examples

Prompts for Copilot

- "Add calculator-related settings to Django settings.py: ROUTE_FACTOR (default 1.2), AVG_SPEED_KMH (default 80), FUEL_PRICE_PER_LITER (default 1.50), FUEL_ECONOMY_L_PER_100KM (default 7.5). Make them configurable via environment variables."
- "Add inline comments explaining what each setting controls and why the defaults were chosen."
- "Generate example .env entries for these settings with explanatory comments."
- "Propose commit message for settings configuration."

Summary

- Status: Completed — calculator defaults added with env overrides, tests, and README docs.
- Files: `travelmathlite/core/settings.py`, `apps/calculators/tests.py`, `travelmathlite/README.md`.
- Tests: 26 tests passing at completion for this slice.
- Commits: [b570b02](https://github.com/ahuimanu/CIDM6325/commit/b570b02) (settings + tests), [1d7ebc7](https://github.com/ahuimanu/CIDM6325/commit/1d7ebc7) (README + brief completion).
- Issue: #45.

---
ADR: adr-1.0.2-geo-calculation-methods.md
PRD: §4 F-001, F-003
Issue: #45
