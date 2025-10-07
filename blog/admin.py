from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","status","published_at","created")
    list_filter = ("status","created","published_at","author")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title","body")
    raw_id_fields = ("author",)
    date_hierarchy = "published_at"
    ordering = ("status","-published_at")


# Register your models here.
