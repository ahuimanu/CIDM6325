Accessibility notes (WCAG 2.2)

This file lists small accessibility checks and improvements for the project.

1. Landmarks and structure
   - `templates/base.html` sets `lang="en"` and exposes a `<main>` with `tabindex="-1"` for skip-to-main keyboard focus.

2. Form labels and errors
   - Ensure form fields render explicit `<label for>` attributes (Django's widgets already create labels). Error messages should be associated with inputs using `aria-describedby` where relevant.

3. Color contrast
   - Bootstrap default color palette is used; ensure contrast for badges and buttons meets 4.5:1 for normal text where required.

4. Keyboard focus
   - HTMX swaps should move focus to newly-inserted controls. Consider adding `hx-vals` or `hx-on` handlers to focus first input after inline-edit is swapped.

5. ARIA and semantics
   - Tables include captions and use `role="table"`. Buttons have `aria-label` where the text is not fully descriptive.

6. Next steps
   - Add `skip to content` link at the top for keyboard-only users.
   - After implementing HTMX inline editing, ensure focus management by adding small JS that listens for `htmx:afterSwap` events and focuses the appropriate element.
