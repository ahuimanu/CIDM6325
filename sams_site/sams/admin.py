from django.contrib import admin
from .models import Item, TeamEvent


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    date_hierarchy = 'created_at'


@admin.register(TeamEvent)
class TeamEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'owner', 'created_at')
    list_filter = ('date', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    date_hierarchy = 'date'
    ordering = ['-date', 'created_at']
