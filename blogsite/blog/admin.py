from django.contrib import admin
from .models import Comment, Post


# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    # Per Mele: Django 5.0 introduces facet filters to the administration site, showcasing facet counts.
    # These counts indicate the number of objects corresponding to each specific filter,
    # making it easier to identify matching objects in the admin changelist view.
    # https://docs.djangoproject.com/en/5.1/releases/5.0/#facet-filters-in-the-admin
    # https://docs.djangoproject.com/en/5.1/ref/contrib/admin/filters/#facet-filters
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
