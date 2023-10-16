from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

"""
we make some light user admin customizations here
"""

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # we'll only display the username field
    fields = ["username"]
    inlines = [ProfileInline]

# register/unregister
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(Profile)