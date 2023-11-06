from django.db import models


# Create your models here.
class Checklist(models.Model):
    name = models.CharField(max_length=150, help_text="Checklist name")


class ChecklistItem(models.Model):
    """An item in a checklist"""

    item = models.TextField(help_text="Checklist item to verify")
    response = models.TextField(help_text="A response to verifiable item")
    checked = models.BooleanField()
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, default=None)
