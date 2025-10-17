from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# Each user can write multiple blog posts (One-to-Many)
class BlogPost(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
        return self.title
  


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# Each post can have multiple comments (One-to-Many)
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
# This code defines two models: BlogPost and Comment.
# The BlogPost model represents a blog post written by a user, while the Comment model represents comments made on those blog posts.
# The relationships are established using ForeignKey fields, indicating that each blog post is authored by a

