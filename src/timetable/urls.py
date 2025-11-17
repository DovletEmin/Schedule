from django.urls import path
from .views import WeekDayScheduleAPIView

urlpatterns = [
    path(
        '<int:week_number>/<int:day_number>/',
        WeekDayScheduleAPIView.as_view(),
        name='week-day-schedule'
    ),
]
