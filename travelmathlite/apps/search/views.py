from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Search app."""

    template_name: str = "search/index.html"
