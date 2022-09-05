from django.db import models

# Create your models here.
class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        # this is list/array slicing
        return self.text[:50]
    