from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import os
from .validators import ImageValidator, validate_image_content


def post_image_upload_path(instance, filename):
    """
    Generate upload path for post images
    Format: posts/post_id/filename
    """
    # Get file extension
    ext = filename.split('.')[-1]
    # Create new filename with post title (if available) or timestamp
    if instance.pk:
        filename = f"post_{instance.pk}_{instance.title[:20]}.{ext}"
    else:
        from django.utils import timezone
        filename = f"post_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    
    # Replace spaces and special characters
    filename = "".join(c for c in filename if c.isalnum() or c in '._-')
    
    return os.path.join('posts', filename)


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(
        upload_to=post_image_upload_path,
        blank=True,
        null=True,
        validators=[ImageValidator(), validate_image_content],
        help_text="Optional image for the blog post (Max 5MB, JPG/PNG/GIF/WebP)"
    )
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Publish date")
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
