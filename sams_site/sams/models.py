from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Item(models.Model):
    """A simple model to illustrate SAMS domain objects."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sams_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TeamEvent(models.Model):
    """Team calendar event model for agenda items on specific dates."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sams_events')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'created_at']

    def __str__(self):
        return f"{self.date}: {self.title}"
