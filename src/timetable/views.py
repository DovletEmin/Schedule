from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Week, Day, TimetableEntry
from .serializers import TimetableEntrySerializer
from .filters import TimetableEntryFilter



class WeekDayScheduleAPIView(APIView):
    def get(self, request, week_number, day_number):
        week = get_object_or_404(Week, number=week_number)

        day = Day.objects.filter(number=day_number).first()
        if not day:
            return Response(
                {"detail": "Day not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        lessons = TimetableEntry.objects.filter(
            week=week,
            day=day
        ).order_by('lesson_number__number')

        serializer = TimetableEntrySerializer(lessons, many=True)

        return Response({
            "week": week.number,
            "day_number": day.number,
            "day_name": day.get_number_display(),
            "schedule": serializer.data
        })
    

    
class TimetableSearchAPIView(ListAPIView):
    queryset = TimetableEntry.objects.select_related(
        'week', 'day', 'group', 'lesson_number', 'subject', 'teacher'
    ).all()
    serializer_class = TimetableEntrySerializer
    filterset_class = TimetableEntryFilter
