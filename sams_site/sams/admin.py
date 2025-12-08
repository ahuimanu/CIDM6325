from django.contrib import admin
from .models import Item, TeamEvent, Announcement, Comment, Student, Attendance


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


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_at')
    list_filter = ('created_at', 'author_name')
    search_fields = ('title', 'content', 'author_name')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'author_name', 'created_at')
    list_filter = ('created_at', 'author_name')
    search_fields = ('content', 'author_name', 'announcement__title')
    date_hierarchy = 'created_at'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'created_at')
    search_fields = ('name', 'student_id')
    ordering = ['name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present', 'recorded_by', 'created_at')
    list_filter = ('date', 'present', 'recorded_by')
    search_fields = ('student__name',)
    date_hierarchy = 'date'
    ordering = ['-date', 'student__name']
