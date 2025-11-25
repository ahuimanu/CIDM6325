import re

import bleach
import markdown
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    "p",
    "a",
    "code",
    "pre",
    "em",
    "strong",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "blockquote",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
}


@register.filter(name="markdown_safe")
def markdown_safe(value: str) -> str:
    """
    Render Markdown to HTML and sanitize output using bleach.
    """
    html = markdown.markdown(value or "", extensions=["fenced_code", "codehilite"])
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    return bleach.linkify(clean_html, callbacks=[bleach.callbacks.nofollow])


@register.filter(name="highlight")
def highlight(text: str, query: str) -> str:
    """Highlight occurrences of `query` within `text` safely.

    - Escapes original text to avoid injecting HTML from content.
    - Wraps case-insensitive matches in <mark class="highlight">…</mark>.
    - Returns safe HTML string.
    """
    if not text or not query:
        return escape(text or "")
    escaped = escape(text)
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f'<mark class="highlight">{m.group(0)}</mark>', escaped)
    return mark_safe(highlighted)
