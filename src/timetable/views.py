from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Week, Day, TimetableEntry
from .serializers import TimetableEntrySerializer, DayScheduleSerializer


class WeekDayScheduleAPIView(APIView):
    def get(self, request, week_number, day_name):
        # 1. Проверяем неделю
        week = get_object_or_404(Week, number=week_number)

        # 2. Находим день (регистронезависимо)
        day = Day.objects.filter(name__iexact=day_name).first()
        if not day:
            return Response(
                {"detail": "Day not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Получаем расписание
        lessons = TimetableEntry.objects.filter(
            week=week,
            day=day
        ).order_by(
            'lesson_number__number'
        )

        # 4. Сериализация расписания
        serializer = TimetableEntrySerializer(lessons, many=True)

        # 5. Формируем финальный объект
        response = {
            "week": week.number,
            "day": day.name,
            "schedule": serializer.data
        }

        return Response(response)
