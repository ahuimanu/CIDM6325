import json
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import Manager


class SavedCalculation(models.Model):
    """
    Store user's last 10 calculator runs with inputs/outputs.

    Fields:
    - user: FK to auth.User
    - calculator_type: type of calculator (e.g., "distance", "cost")
    - inputs: JSON TextField storing input values
    - outputs: JSON TextField storing calculated results
    - created_at: timestamp for ordering and pruning

    Pruning: On save, if user has >10 entries, oldest are deleted.
    """

    if TYPE_CHECKING:
        objects: "Manager[SavedCalculation]"  # type: ignore[assignment]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_calculations",
    )
    calculator_type = models.CharField(
        max_length=50,
        help_text="Type of calculator (e.g., distance, cost, time)",
    )
    inputs = models.TextField(help_text="JSON-serialized input values")
    outputs = models.TextField(help_text="JSON-serialized calculation results")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.calculator_type} ({self.created_at})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save and enforce max 10 entries per user by pruning oldest."""
        super().save(*args, **kwargs)

        # Get count of user's saved calculations
        user_calcs = SavedCalculation.objects.filter(user=self.user).order_by("-created_at")
        count = user_calcs.count()

        # If more than 10, delete the oldest ones
        if count > 10:
            # Get IDs of entries beyond the 10 most recent
            ids_to_keep = list(user_calcs.values_list("id", flat=True)[:10])
            SavedCalculation.objects.filter(user=self.user).exclude(id__in=ids_to_keep).delete()

    def get_inputs(self) -> dict:
        """Return inputs as dict."""
        try:
            return json.loads(str(self.inputs))
        except json.JSONDecodeError:
            return {}

    def get_outputs(self) -> dict:
        """Return outputs as dict."""
        try:
            return json.loads(str(self.outputs))
        except json.JSONDecodeError:
            return {}

    def set_inputs(self, data: dict) -> None:
        """Store inputs from dict."""
        self.inputs = json.dumps(data)

    def set_outputs(self, data: dict) -> None:
        """Store outputs from dict."""
        self.outputs = json.dumps(data)
