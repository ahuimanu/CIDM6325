from django.contrib import admin
from .models import Post, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "created_at", "updated_at")
    list_filter = ("status", "author", "tags")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    # show related objects efficiently
    list_select_related = ("author",)
    # allow quick actions in the admin list view
    actions = ["make_published"]

    def make_published(self, request, queryset):
        """Admin action to bulk-publish selected posts."""
        updated = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f"{updated} post(s) marked as published.")
    make_published.short_description = "Mark selected posts as published"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("user", "body", "created_at", "is_approved")
    readonly_fields = ("created_at",)

    def has_delete_permission(self, request, obj=None):
        # allow deletion via the inline only for staff with delete permission
        return request.user.has_perm("blog.delete_comment")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "post_count")
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # annotate post counts to avoid extra queries in list view
        return qs

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "Posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("short_body", "post", "user", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("body", "user__username", "post__title")
    date_hierarchy = "created_at"
    list_select_related = ("post", "user")

    def short_body(self, obj):
        return (obj.body[:75] + "...") if len(obj.body) > 75 else obj.body
    short_body.short_description = "Comment"

    actions = ["approve_comments", "disapprove_comments"]

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} comment(s) disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"

# Add the comment inline to PostAdmin so editors can moderate while editing a post
PostAdmin.inlines = [CommentInline]
