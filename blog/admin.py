from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","status","published_at","created_at")
    list_filter = ("status","created_at","published_at","author")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title","body","slug")
    autocomplete_fields = ["author"]
    date_hierarchy = "published_at"
    ordering = ("status","-published_at")


# Register your models here.
