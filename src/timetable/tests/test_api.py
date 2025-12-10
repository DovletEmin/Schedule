import pytest
from rest_framework.test import APIClient
from timetable.models import (
    Faculty,
    Course,
    Group,
    Week,
    Day,
    Teacher,
    LessonNumber,
    LessonType,
    Subject,
    TimetableEntry,
)


@pytest.mark.django_db
def test_week_day_schedule_api():
    client = APIClient()

    faculty = Faculty.objects.create(name="Informatics")
    course = Course.objects.create(number=1, faculty=faculty)
    group = Group.objects.create(name="A", course=course)
    week = Week.objects.create(number=1)
    day = Day.objects.create(number=1)
    teacher = Teacher.objects.create(name="Ali")
    lesson_number = LessonNumber.objects.create(number=1)
    lesson_type = LessonType.objects.create(name="Lecture")
    subject = Subject.objects.create(name="Math")

    TimetableEntry.objects.create(
        week=week,
        day=day,
        group=group,
        lesson_number=lesson_number,
        subject=subject,
        teacher=teacher,
        lesson_type=lesson_type,
        room="101",
    )

    response = client.get(f"/api/{week.number}/{day.number}/")

    assert response.status_code == 200
    data = response.json()
    assert data["week"] == 1
    assert data["day_number"] == 1
    assert len(data["schedule"]) == 1
    assert data["schedule"][0]["subject"] == "Math"


@pytest.mark.django_db
def test_timetable_search_api():
    client = APIClient()

    faculty = Faculty.objects.create(name="Informatics")
    course = Course.objects.create(number=1, faculty=faculty)
    group = Group.objects.create(name="A", course=course)
    week = Week.objects.create(number=1)
    day = Day.objects.create(number=1)
    teacher = Teacher.objects.create(name="Ali")
    lesson_number = LessonNumber.objects.create(number=1)
    lesson_type = LessonType.objects.create(name="Lecture")
    subject = Subject.objects.create(name="Math")

    TimetableEntry.objects.create(
        week=week,
        day=day,
        group=group,
        lesson_number=lesson_number,
        subject=subject,
        teacher=teacher,
        lesson_type=lesson_type,
        room="101",
    )

    response = client.get("/api/search/?teacher=Ali")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["teacher"] == "Ali"
