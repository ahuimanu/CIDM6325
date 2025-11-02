from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Trips app."""

    template_name: str = "trips/index.html"
