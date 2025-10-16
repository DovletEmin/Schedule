from django.contrib import admin
from .models import *

# Базовый админ для моделей без специфичных настроек
@admin.register(Faculty, Course, Teacher, Subject, Day, Week, LessonNumber)
class BaseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

# Inline для расписания в админке групп
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

# Кастомная админка для Group с inline
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__',)  # Наследуем отображение из BaseAdmin
    inlines = [ScheduleInline]

# Админка для Schedule
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'day', 'week', 'lesson_number', 'subject', 'teacher', 'lesson_type')
    list_filter = ('group', 'day', 'week')
    search_fields = ('subject__name', 'teacher__full_name')