# Weeks 7–8: CBV Refactor & Tradeoffs

## What changed
- Converted FBVs to CBVs (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).
- Mixins used: `LoginRequiredMixin`, `PermissionRequiredMixin`, custom `AuthorRequiredMixin`, and `HtmxQueryMixin`.
- Reduced repetitive logic and centralized responsibilities.

## Tradeoffs (FBV vs CBV)
- **FBV Pros:** Simple flow; easy for small features. **Cons:** Repetition.
- **CBV Pros:** Inheritance, DRY, hook methods; **Cons:** Indirection can obscure flow.

## AI Disclosure
Prompts used to design mixins and select hook methods. I validated outputs against Django 5 docs and rejected deprecated patterns.
