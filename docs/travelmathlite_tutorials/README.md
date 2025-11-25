# TravelMathLite Tutorials (by ADR)

This folder hosts short, repeatable tutorials for each ADR. After finishing an ADR, create a tutorial under `docs/travelmathlite_tutorials/adr-<id>/` using the template.

- See the ongoing brief: `docs/travelmathlite/briefs/brief-ongoing-tutorials.md`.
- Use the template: `docs/travelmathlite_tutorials/tutorial_brief_template_v1.0.0.md`.

## How to add a tutorial

1. Identify the ADR id (e.g., `1.0.3`).
2. Read the ADR and its briefs in `docs/travelmathlite/briefs/adr-<id>/`.
3. Copy the template to `docs/travelmathlite_tutorials/adr-<id>/tutorial-ADR-<id>-<slug>.md`.
4. Fill the template with:
   - Goals, prerequisites, and steps (guided by briefs)
   - Copy‑pasteable commands and minimal code snippets
   - References to Django docs, Bootstrap, HTMX, and Matt Layman’s Understand Django
5. Commit as `docs: add tutorial for ADR-<id>`.

## References

- [Understand Django (Matt Layman)](https://www.mattlayman.com/understand-django/)
- [Django documentation](https://docs.djangoproject.com/)
- [Bootstrap documentation](https://getbootstrap.com/docs/)
- [HTMX documentation](https://htmx.org/docs/)
