from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Core app."""

    template_name: str = "core/index.html"
