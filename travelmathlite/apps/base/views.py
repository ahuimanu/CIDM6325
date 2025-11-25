from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Base app."""

    template_name: str = "base/index.html"
