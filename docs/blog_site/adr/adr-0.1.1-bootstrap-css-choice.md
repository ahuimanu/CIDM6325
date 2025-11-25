# ADR-0.1.1: Choose Bootstrap 5 CDN for Styling

Date: 2025-10-19
Status: Accepted

Context

- PRD v1.0.1 §13 posed an open question: Tailwind CLI vs no-build CSS framework (A: Bootstrap).
- Teaching constraint: keep setup simple (no Node build chain) and prioritize rapid iteration in class.
- Current implementation already uses a lightweight base template and CDN assets.

Options

- A) Tailwind CSS via CLI/build pipeline
- B) PicoCSS (no-build, minimal styling)
- C) Bootstrap 5 via CDN (no-build)

Decision

- Choose C) Bootstrap 5 via CDN.

Rationale

- No build step simplifies classroom setup and repo complexity.
- Bootstrap provides robust components and responsive grid out of the box.
- Aligns with PRD non-goal of avoiding heavy front-end frameworks while meeting responsiveness.

Consequences

- Positive: Fast prototyping, consistent UI utilities, fewer moving parts.
- Negative/Risks: Heavier than Pico; design may feel generic without customization.

Validation

- Base template includes Bootstrap 5 CDN; forms use Bootstrap classes; pages render responsively.
- Rollback: Replace with PicoCSS or add Tailwind later if design flexibility becomes a priority.
