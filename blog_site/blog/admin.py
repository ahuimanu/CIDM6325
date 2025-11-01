from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "publish_date")
    search_fields = ("title", "body")
    #prepopulated_fields = {"slug": ("title",)}
    change_form_template = "admin/blog/post/change_form.html"
