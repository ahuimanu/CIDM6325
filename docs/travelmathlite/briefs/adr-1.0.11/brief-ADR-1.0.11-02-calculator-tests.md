# BRIEF: Build calculator unit tests slice

Goal

- Implement unit tests for calculator functions (distance, cost, nearest airport) addressing PRD §4 F-011.

Scope (single PR)

- Files to touch: `travelmathlite/apps/calculators/tests.py` or `travelmathlite/apps/calculators/tests/test_geo.py`, `travelmathlite/apps/calculators/tests/test_costs.py`.
- Behavior: Test calculation logic in isolation; cover happy paths and edge cases (e.g., invalid coordinates, zero distance, boundary values).
- Non-goals: View/form testing (separate brief), integration tests.

Standards

- Commits: conventional style (test).
- Use `uv run` for Django commands; lint/format with Ruff.
- Django tests: use Django TestCase (no pytest).

Acceptance

- User flow: Run `uv run python manage.py test calculators` and see all calculator logic tests pass.
- Tests cover distance calculation, cost estimation, nearest airport search with 1-2 edge cases each.
- No external API calls during tests (mock if needed).
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create unit tests in `apps/calculators/tests/test_geo.py` for distance calculation functions with happy path and edge cases (invalid coords, same location)."
- "Create unit tests in `apps/calculators/tests/test_costs.py` for cost estimation with positive cases and boundary values (zero distance, negative costs)."
- "Add tests for nearest airport search logic covering valid results and empty results scenarios."
- "Ensure all tests are deterministic and isolated; mock any external data sources."

---
ADR: adr-1.0.11-testing-strategy.md
PRD: §4 F-011
Requirements: FR-F-011-1
Invariants: INV-1 (tests deterministic and isolated)
