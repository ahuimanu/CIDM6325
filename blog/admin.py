from django.contrib import admin
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'tags', 'created_at')
    search_fields = ('title', 'body', 'author__username')
    autocomplete_fields = ('author', 'category', 'tags')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('title', 'body', 'image')}),
        ('Classification', {'fields': ('category', 'tags', 'is_published')}),
        ('Ownership', {'fields': ('author',)}),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'post', 'author', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    autocomplete_fields = ('post', 'author')
    def short_content(self, obj): 
        return (obj.content[:60] + '…') if len(obj.content) > 60 else obj.content
    short_content.short_description = 'Content'
