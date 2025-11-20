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
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sams_events')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time', 'created_at']

    def __str__(self):
        return f"{self.date}: {self.title}"
    
    def has_time_conflict(self):
        """Check if this event's time range conflicts with other events on the same day."""
        if not self.start_time or not self.end_time:
            return False
        
        # Get other events on the same date
        same_day_events = TeamEvent.objects.filter(
            date=self.date
        ).exclude(id=self.id)
        
        for event in same_day_events:
            if event.start_time and event.end_time:
                # Check for overlap: event starts before this ends AND event ends after this starts
                if (event.start_time < self.end_time and event.end_time > self.start_time):
                    return True
        
        return False


class Announcement(models.Model):
    """Public blog post model where anyone can post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments on blog posts."""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, default="Anonymous")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.announcement.title}"
