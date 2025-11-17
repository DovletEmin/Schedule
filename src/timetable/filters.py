import django_filters
from .models import TimetableEntry


class TimetableEntryFilter(django_filters.FilterSet):
    teacher = django_filters.CharFilter(field_name="teacher__name", lookup_expr="icontains")
    week = django_filters.NumberFilter(field_name="week__number")
    day = django_filters.NumberFilter(field_name="day__number")
    group = django_filters.CharFilter(field_name="group__name", lookup_expr="icontains")
    lesson_number = django_filters.NumberFilter(field_name="lesson_number__number")
    faculty = django_filters.CharFilter(field_name="group__course__faculty__name", lookup_expr="icontains")
    course = django_filters.NumberFilter(field_name="group__course__number") 

    class Meta:
        model = TimetableEntry
        fields = ['teacher', 'week', 'day', 'group', 'lesson_number', 'faculty', 'course']
