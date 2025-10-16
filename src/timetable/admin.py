from django.contrib import admin
from .models import *

@admin.register(Faculty, Course, Teacher, Subject, Day, Week, Room)
class BaseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [ScheduleInline]

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'day', 'week', 'lesson_number', 'subject', 'teacher', 'room', 'lesson_type')
    list_filter = ('group', 'day', 'week', 'room')
    search_fields = ('subject__name', 'teacher__full_name', 'room__name')

@admin.register(LessonNumber)
class LessonNumberAdmin(admin.ModelAdmin):
    list_display = ('pair_number', 'start_time', 'end_time')