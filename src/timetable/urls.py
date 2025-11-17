from django.urls import path
from .views import WeekDayScheduleAPIView

urlpatterns = [
    path('week/<int:week_number>/<str:day_name>/', WeekDayScheduleAPIView.as_view()),
]
