from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from timetable.views import TimetableEntryViewSet, SubjectViewSet


router = routers.DefaultRouter()
router.register(r'entries', TimetableEntryViewSet)
router.register(r'subjects', SubjectViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]