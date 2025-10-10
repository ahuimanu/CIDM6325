from django.contrib import admin
from .models import Post, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "updated_at")
    list_filter = ("status", "author", "tags")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Tag)
admin.site.register(Comment)
