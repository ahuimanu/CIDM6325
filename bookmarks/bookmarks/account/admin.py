from django.contrib import admin
from . models import Profile

# Register your models here.
from django.contrib import admin
from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
