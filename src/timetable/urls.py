from django.urls import path
from .views import TimetableSearchAPIView, WeekDayScheduleAPIView, WeekScheduleAPIView, timetable_view, timetable_grid

urlpatterns = [
    # API endpoints
    path(
        '<int:week_number>/<int:day_number>/',
        WeekDayScheduleAPIView.as_view(),
        name='week-day-schedule'
    ),
    path(
        '<int:week_number>/',
        WeekScheduleAPIView.as_view(),
        name='week-schedule'
    ),
    path("search/", TimetableSearchAPIView.as_view(), name="timetable-search"),
]
