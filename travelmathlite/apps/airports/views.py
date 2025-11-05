from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Airports app."""

    template_name: str = "airports/index.html"
