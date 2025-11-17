from django.contrib import admin
from .models import *


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('number', 'faculty')
    list_filter = ('faculty',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course__faculty', 'course__number')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('number',)
    ordering = ('number',)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(LessonNumber)
class LessonNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_time', 'end_time')
    ordering = ('number',)


@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = (
        'week', 
        'day', 
        'group', 
        'lesson_number', 
        'subject', 
        'teacher', 
        'lesson_type', 
        'room'
    )
    list_filter = (
        'week',
        'day',
        'group__course__faculty',
        'group__course__number',
    )
    search_fields = (
        'subject__name',
        'teacher__name',
        'group__name'
    )
