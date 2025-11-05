from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Minimal index landing page for the Accounts app."""

    template_name: str = "accounts/index.html"
