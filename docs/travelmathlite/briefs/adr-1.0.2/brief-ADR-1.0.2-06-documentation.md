# BRIEF: Build documentation slice

Goal

- Document algorithms, formulas, and usage for distance and cost calculators addressing PRD §4 F-001, F-003.

Scope (single PR)

- Files to touch: `docs/travelmathlite/algorithms/distance-and-cost.md`, README updates.
- Non-goals: Implementation code changes.

Standards

- Commits: conventional style (docs).
- Clear explanations for non-technical readers; include formulas and examples.

Acceptance

- User flow: Developer or user can read documentation to understand calculation methods and assumptions.
- Documentation includes: formulas, default values, example inputs/outputs, limitations.
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [ ] Create `docs/travelmathlite/algorithms/distance-and-cost.md`:
  - **Distance calculations**:
    - Haversine/geodesic formula explanation
    - Heuristic for driving distance: `driving_distance = straight_line_km × route_factor`
    - Default route_factor = 1.2 (rationale: accounts for non-straight roads)
  - **Time calculations**:
    - Formula: `driving_time_hours = driving_distance_km / avg_speed_kmh`
    - Default avg_speed_kmh = 80 (rationale: mixed highway/urban)
  - **Cost calculations**:
    - Formula: `fuel_cost = (distance_km / 100) × fuel_economy_l_per_100km × fuel_price_per_liter`
    - Default fuel economy = 7.5 L/100km
    - Default fuel price = €1.50/L
  - **Unit conversions**:
    - km ↔ miles: 1 mile = 1.60934 km
    - MPG ↔ L/100km: `L/100km = 235.214 / MPG`
    - gallons ↔ liters: 1 gallon = 3.78541 liters
  - **Examples**:
    - NYC to LA: ~3,944 km flight, ~4,733 km driving (route factor 1.2), ~59 hours drive (at 80 km/h)
  - **Limitations and assumptions**:
    - No real-time routing; heuristic-based
    - Assumes average conditions; actual may vary
- [ ] Update `README.md` or quickstart guide:
  - Link to algorithms doc
  - Example usage of distance and cost calculators
  - Screenshots or example inputs/outputs (optional)
- [ ] Ensure doc formatting (Markdown) and links are correct

Prompts for Copilot

- "Generate documentation file `docs/travelmathlite/algorithms/distance-and-cost.md` explaining distance, time, and cost calculation methods. Include formulas, default values, rationale, examples, and limitations."
- "Add unit conversion formulas and examples to the documentation."
- "Update README.md with a section on calculators: brief description and link to detailed algorithms doc."
- "Propose commit message for documentation updates."

---
ADR: adr-1.0.2-geo-calculation-methods.md
PRD: §4 F-001, F-003
Issue: #TODO
