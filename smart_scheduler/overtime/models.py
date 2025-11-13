from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class OvertimeEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="overtime_entries",
    )
    # the day the overtime was worked
    shift_date = models.DateField(default=timezone.localdate)
    # overtime hours for that day (e.g., 2.5)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.CharField(max_length=200, blank=True)
    approved_on = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-shift_date"]

    def __str__(self):
        return f"{self.user} — {self.shift_date} (+{self.hours}h)"

    @property
    def week_start(self):
        """Convenience: Monday of the week for this entry."""
        d = self.shift_date
        return d - timedelta(days=d.weekday())
