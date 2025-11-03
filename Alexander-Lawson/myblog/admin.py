from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "date_created", "date_updated")
	search_fields = ("title", "content")
	list_filter = ("author", "date_created")
	ordering = ("-date_created",)
	# Make 'date_created' editable in the admin form
	fieldsets = (
		(None, {
			'fields': ("title", "author", "content", "date_created", "date_updated")
		}),
	)
	# Only date_updated is read-only; date_created (publish date) is editable
	readonly_fields = ("date_updated",)

# Customize User admin for author management
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)
    
# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
