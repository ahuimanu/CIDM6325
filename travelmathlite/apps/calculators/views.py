from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Calculators app."""

    template_name: str = "calculators/index.html"
