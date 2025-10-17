from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ['name']
    def __str__(self): return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self): return self.name

class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = [('can_publish', 'Can publish posts')]
        ordering = ['-created_at']
    def __str__(self): return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']
    def __str__(self): return f"Comment by {self.author or 'Anonymous'} on {self.post}"
