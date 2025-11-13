from rest_framework import viewsets, filters
from .models import TimetableEntry, Subject
from .serializers import TimetableEntrySerializer, SubjectSerializer


class TimetableEntryViewSet(viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.select_related(
    'subject', 'teacher', 'group', 'lesson_number', 'lesson_type', 'day', 'week'
    )
    serializer_class = TimetableEntrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject__name', 'teacher__last_name']
    ordering_fields = ['week', 'day__order', 'lesson_number__number']


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer