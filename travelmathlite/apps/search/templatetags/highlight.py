"""Highlight filter for safe query highlighting in templates."""

from __future__ import annotations

import re
from typing import Any

from django import template
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def highlight(text: Any, query: str | None, autoescape: bool = True) -> str:
    """Wrap case-insensitive matches of query in <mark> tags safely.

    Ensures the base text is escaped, then injects only safe <mark> wrappers.
    This preserves Django's autoescape behavior (INV-2 from ADR-1.0.4).

    Args:
        text: The text to search and highlight.
        query: The search term to highlight (case-insensitive).
        autoescape: Whether to escape text (provided by Django).

    Returns:
        SafeString with <mark> around matches, or original text if no query.
    """
    if not query or not text:
        # Return text as-is, respecting autoescape
        if autoescape:
            return str(conditional_escape(text))
        return str(text)

    text_str = str(text)
    query_str = str(query).strip()

    if not query_str:
        if autoescape:
            return str(conditional_escape(text_str))
        return text_str

    # Escape the base text first
    if autoescape:
        escaped_text = conditional_escape(text_str)
    else:
        escaped_text = text_str

    # Escape the query for use in regex (防止regex injection)
    escaped_query = re.escape(query_str)

    # Find all case-insensitive matches and wrap with <mark>
    # Use a lambda to preserve the original case of the matched text
    def replace_fn(match: re.Match[str]) -> str:
        return format_html("<mark>{}</mark>", match.group(0))

    highlighted = re.sub(
        f"({escaped_query})",
        replace_fn,
        str(escaped_text),
        flags=re.IGNORECASE,
    )

    return mark_safe(highlighted)
