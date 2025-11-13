from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Post


# 1) BLOG POST ADMIN (your custom model)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "published_at",
        "created_at",
    )
    list_filter = (
        "status",
        "author",
        "published_at",
        "created_at",
    )
    search_fields = ("title", "body", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)


# 2) USER ADMIN (built-in model) — keep it simple
# Django already registers User, so unregister first
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # these are REAL fields on auth.User
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


