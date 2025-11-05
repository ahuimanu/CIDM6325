# ADR-0.1.2: Markdown Rendering Stack (Python-Markdown + Bleach)

Date: 2025-10-19
Status: Accepted

Context

- PRD v1.0.1 lists markdown-it-py + Pygments as preferred for syntax highlighting (F-003).
- Our implementation uses Python-Markdown with extensions + Bleach sanitization via a Django template filter (`blog/templatetags/markdown_extras.py`).
- Goal: capture the rationale for this divergence and document a migration path if we adopt markdown-it-py later.

Options

- A) markdown-it-py + Pygments (aligns with PRD)
- B) Python-Markdown + Bleach (current)
- C) Markdown2 + custom sanitizer

Decision

- Choose B) Python-Markdown + Bleach for MVP.

Rationale

- Python-Markdown is widely used, simple to integrate, and pairs well with Bleach for robust HTML sanitization.
- Minimal dependencies, easy to unit test, and good enough for teaching the render/sanitize pipeline.
- We can enable code blocks now; syntax highlighting can be added later with Pygments or a client-side highlighter.

Consequences

- Positive: Straightforward integration, secure-by-default sanitization, test coverage already in place.
- Negative/Risks: Lacks the richer plugin ecosystem of markdown-it; server-side highlighting not yet enabled.

Validation

- `test_post_detail_renders_markdown_safely` verifies rendered `**bold**` output and links, and that script tags are removed.
- Rollback/Upgrade: To align with PRD, swap the renderer to markdown-it-py and add Pygments; keep Bleach for sanitization or constrain renderer to safe output.
