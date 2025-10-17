import markdown
import bleach
from django import template

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
