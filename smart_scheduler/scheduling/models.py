from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class Shift(models.Model):
    class Status(models.TextChoices):
        OPEN      = "open", "Open"
        ASSIGNED  = "assigned", "Assigned"

    role      = models.CharField(max_length=80, blank=True)          # e.g., Dispatcher, Lead, ERT
    location  = models.CharField(max_length=120, blank=True)         # optional
    starts_at = models.DateTimeField()
    ends_at   = models.DateTimeField()
    status    = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="shifts"
    )

    def clean(self):
        if self.ends_at <= self.starts_at:
            raise ValidationError("Shift end must be after start.")
        # If assigned, mark assigned
        if self.assigned_to and self.status == self.Status.OPEN:
            self.status = self.Status.ASSIGNED

    def duration_hours(self):
        delta = self.ends_at - self.starts_at
        return round(delta.total_seconds() / 3600.0, 2)

    def __str__(self):
        who = self.assigned_to or "Unassigned"
        return f"{self.starts_at:%Y-%m-%d %H:%M} → {self.ends_at:%H:%M} • {who}"

class Availability(models.Model):
    """
    Minimal availability window: a single day + flag.
    (Later you can extend to start/end DateTime windows.)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user} • {self.date} • {'Available' if self.is_available else 'Not available'}"


# Create your models here.
