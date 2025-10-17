from django.contrib import admin

# Register your models here.

from .models import BlogPost, Comment

admin.site.register(BlogPost)
admin.site.register(Comment)

# This code registers the BlogPost and Comment models with the Django admin site,
# allowing administrators to manage blog posts and comments through the admin interface. 