from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager

class Post(models.Model):
    """
    Blog post model for CIDM 6325 example.
    """
    title: str = models.CharField(max_length=200, unique=True)
    slug: str = models.SlugField(max_length=220, unique=True, editable=False)
    body: str = models.TextField(help_text="Markdown content")
    publish_date: timezone.datetime = models.DateTimeField(default=timezone.now)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-publish_date"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        """
        Generate slug from title if not set.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        String representation of the post.
        """
        return self.title

