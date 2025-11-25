from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView

from .models import SavedCalculation


class IndexView(TemplateView):
    """Minimal index landing page for the Trips app."""

    template_name: str = "trips/index.html"


class SavedCalculationListView(LoginRequiredMixin, ListView):
    """
    List view for user's saved calculations.

    Only shows calculations owned by the current user, ordered newest first.
    Enforces login via LoginRequiredMixin.
    """

    model = SavedCalculation
    template_name = "trips/saved_list.html"
    context_object_name = "calculations"
    paginate_by = 10

    def get_queryset(self):
        """Filter to only show current user's calculations."""
        return SavedCalculation.objects.filter(user=self.request.user).order_by("-created_at")


class SavedCalculationDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view for saved calculations with ownership validation.

    Only allows users to delete their own calculations.
    Returns 404 if trying to access another user's calculation.
    """

    model = SavedCalculation
    template_name = "trips/saved_confirm_delete.html"
    success_url = reverse_lazy("trips:saved_list")

    def get_queryset(self):
        """Filter to only allow deletion of current user's calculations."""
        return SavedCalculation.objects.filter(user=self.request.user)
