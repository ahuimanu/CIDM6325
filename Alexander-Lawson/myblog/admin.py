from django.contrib import admin

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
