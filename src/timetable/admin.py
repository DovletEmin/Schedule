from django.contrib import admin
from .models import *

@admin.register(Faculty, Course, Teacher, Subject, Day, Week, LessonNumber, Room)
class BaseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [ScheduleInline]

# Админка для Schedule
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'day', 'week', 'lesson_number', 'subject', 'teacher', 'room', 'lesson_type')
    list_filter = ('group', 'day', 'week', 'room')
    search_fields = ('subject__name', 'teacher__full_name')