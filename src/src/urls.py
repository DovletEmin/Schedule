from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from timetable.views import timetable_view, timetable_grid

urlpatterns = [
    path("admin/", admin.site.urls),
    # Frontend
    path("", timetable_grid, name="timetable_grid"),
    path("list/", timetable_view, name="timetable_view"),
    # API
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("timetable.urls")),
]
