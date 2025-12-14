from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render

from .models import (
    Week,
    Day,
    TimetableEntry,
    Faculty,
    Course,
    Group,
    Teacher,
    LessonNumber,
)
from .serializers import TimetableEntrySerializer
from .filters import TimetableEntryFilter


class WeekDayScheduleAPIView(APIView):
    def get(self, request, week_number, day_number):
        week = get_object_or_404(Week, number=week_number)

        day = Day.objects.filter(number=day_number).first()
        if not day:
            return Response(
                {"detail": "Day not found"}, status=status.HTTP_404_NOT_FOUND
            )

        lessons = TimetableEntry.objects.filter(week=week, day=day).order_by(
            "lesson_number__number"
        )

        serializer = TimetableEntrySerializer(lessons, many=True)

        return Response(
            {
                "week": week.number,
                "day_number": day.number,
                "day_name": day.get_number_display(),
                "schedule": serializer.data,
            }
        )


class WeekScheduleAPIView(APIView):
    def get(self, request, week_number):
        week = get_object_or_404(Week, number=week_number)

        lessons = TimetableEntry.objects.filter(
            week=week,
        ).order_by("lesson_number__number")

        serializer = TimetableEntrySerializer(lessons, many=True)

        return Response({"week": week.number, "schedule": serializer.data})


class TimetableSearchAPIView(ListAPIView):
    queryset = TimetableEntry.objects.select_related(
        "week", "day", "group", "lesson_number", "subject", "teacher"
    ).all()
    serializer_class = TimetableEntrySerializer
    filterset_class = TimetableEntryFilter


# Frontend Views
def timetable_view(request):
    """Main timetable view with filters"""
    # Get all filter options
    faculties = Faculty.objects.all().order_by("name")
    courses = Course.objects.all().order_by("number")
    groups = Group.objects.all().order_by("name")
    teachers = Teacher.objects.all().order_by("name")
    weeks = Week.objects.all().order_by("number")
    days = Day.objects.all().order_by("number")

    # Get selected filters from request
    selected_faculty = request.GET.get("faculty", "")
    selected_course = request.GET.get("course", "")
    selected_group = request.GET.get("group", "")
    selected_teacher = request.GET.get("teacher", "")
    selected_week = request.GET.get("week", "")
    selected_day = request.GET.get("day", "")

    # Filter courses based on selected faculty
    if selected_faculty:
        courses = courses.filter(faculty_id=selected_faculty)

    # Filter groups based on selected course
    if selected_course:
        groups = groups.filter(course_id=selected_course)

    # Build query for timetable entries
    entries = TimetableEntry.objects.select_related(
        "week",
        "day",
        "group",
        "group__course",
        "group__course__faculty",
        "lesson_number",
        "subject",
        "teacher",
        "lesson_type",
    ).all()

    # Apply filters
    if selected_faculty:
        entries = entries.filter(group__course__faculty_id=selected_faculty)

    if selected_course:
        entries = entries.filter(group__course_id=selected_course)

    if selected_group:
        entries = entries.filter(group_id=selected_group)

    if selected_teacher:
        entries = entries.filter(teacher_id=selected_teacher)

    if selected_week:
        entries = entries.filter(week_id=selected_week)

    if selected_day:
        entries = entries.filter(day_id=selected_day)

    # Special handling for "Ahli" (all weeks) filter
    week1_entries = week2_entries = None
    if not selected_week or selected_week == "ahli" or selected_week == "0":
        week1_entries = entries.filter(week__number=1).order_by(
            "week__number",
            "group__course__faculty__id",
            "group__course__number",
            "group__name",
            "day__number",
            "lesson_number__number",
        )
        week2_entries = entries.filter(week__number=2).order_by(
            "week__number",
            "group__course__faculty__id",
            "group__course__number",
            "group__name",
            "day__number",
            "lesson_number__number",
        )
        context = {
            "faculties": faculties,
            "courses": courses,
            "groups": groups,
            "teachers": teachers,
            "weeks": weeks,
            "days": days,
            "week1_entries": week1_entries,
            "week2_entries": week2_entries,
            "entries": None,
            "selected_faculty": selected_faculty,
            "selected_course": selected_course,
            "selected_group": selected_group,
            "selected_teacher": selected_teacher,
            "selected_week": selected_week,
            "selected_day": selected_day,
        }
    else:
        entries = entries.order_by(
            "week__number",
            "group__course__faculty__id",
            "group__course__number",
            "group__name",
            "day__number",
            "lesson_number__number",
        )
        context = {
            "faculties": faculties,
            "courses": courses,
            "groups": groups,
            "teachers": teachers,
            "weeks": weeks,
            "days": days,
            "entries": entries,
            "week1_entries": None,
            "week2_entries": None,
            "selected_faculty": selected_faculty,
            "selected_course": selected_course,
            "selected_group": selected_group,
            "selected_teacher": selected_teacher,
            "selected_week": selected_week,
            "selected_day": selected_day,
        }

    return render(request, "timetable.html", context)


def timetable_grid(request):
    """Grid view of timetable - Excel-like format with days as rows and lesson numbers as columns"""
    # Get all filter options
    faculties = Faculty.objects.all().order_by("name")
    courses = Course.objects.all().order_by("number")
    teachers = Teacher.objects.all().order_by("name")
    weeks = Week.objects.all().order_by("number")
    days = Day.objects.all().order_by("number")

    # Get selected filters
    selected_faculty = request.GET.get("faculty", "")
    selected_course = request.GET.get("course", "")
    selected_teacher = request.GET.get("teacher", "")
    selected_week = request.GET.get("week", "")
    selected_day = request.GET.get("day", "")

    # Filter courses based on selected faculty
    if selected_faculty:
        courses = courses.filter(faculty_id=selected_faculty)

    # Filter teachers based on selected faculty and course (FIXED: filter through timetableentry__group__course)
    if selected_faculty:
        teachers = (
            Teacher.objects.filter(
                timetableentry__group__course__faculty_id=selected_faculty
            )
            .distinct()
            .order_by("name")
        )
    elif selected_course:
        teachers = (
            Teacher.objects.filter(timetableentry__group__course_id=selected_course)
            .distinct()
            .order_by("name")
        )
    else:
        teachers = Teacher.objects.all().order_by("name")

    # Get courses for query
    courses_query = (
        Course.objects.select_related("faculty")
        .all()
        .order_by("faculty__name", "number")
    )
    if selected_faculty:
        courses_query = courses_query.filter(faculty_id=selected_faculty)
    if selected_course:
        courses_query = courses_query.filter(id=selected_course)

    # If teacher is selected, filter courses that have lessons from this teacher
    if selected_teacher:
        courses_with_teacher = (
            TimetableEntry.objects.filter(teacher_id=selected_teacher)
            .values_list("group__course_id", flat=True)
            .distinct()
        )
        courses_query = courses_query.filter(id__in=courses_with_teacher)

    selected_week_obj = None
    if selected_week:
        try:
            selected_week_obj = Week.objects.get(id=selected_week)
        except (Week.DoesNotExist, ValueError):
            pass

    selected_day_obj = None
    if selected_day:
        selected_day_obj = Day.objects.get(id=selected_day)

    # Разделение по неделям, если выбран "Ahli" или "" (все)
    week1_courses_data = []
    week2_courses_data = []
    all_courses_data = []

    for course in courses_query:
        groups = Group.objects.filter(course=course).order_by("name")
        if not groups.exists():
            continue

        group_names = [g.name for g in groups]
        entries_query = TimetableEntry.objects.select_related(
            "week", "day", "group", "lesson_number", "subject", "teacher", "lesson_type"
        ).filter(group__course=course, group__in=groups)
        if selected_day:
            entries_query = entries_query.filter(day_id=selected_day)

        # Для week1
        week1_entries = entries_query.filter(week__number=1).order_by(
            "day__number", "lesson_number__number", "group__name"
        )
        # Для week2
        week2_entries = entries_query.filter(week__number=2).order_by(
            "day__number", "lesson_number__number", "group__name"
        )
        # Для обычного режима (конкретная неделя)
        filtered_entries = entries_query
        if selected_week and selected_week != "ahli" and selected_week != "":
            try:
                filtered_entries = filtered_entries.filter(week_id=selected_week)
            except (ValueError, TypeError):
                pass

        # Функция для построения timetable_data
        def build_timetable(entries, group_order=None, selected_teacher_id=None):
            lesson_numbers = entries.values_list("lesson_number", flat=True).distinct()
            lesson_number_objs = LessonNumber.objects.filter(
                id__in=lesson_numbers
            ).order_by("number")
            timetable_data = {}
            for day in days:
                day_entries = entries.filter(day=day)
                if not day_entries.exists():
                    continue
                lesson_data = {}
                for lesson_num_obj in lesson_number_objs:
                    lesson_entries = day_entries.filter(lesson_number=lesson_num_obj)
                    if not lesson_entries.exists():
                        continue
                    first_entry = lesson_entries.first()
                    is_same_subject = all(
                        e.subject_id == first_entry.subject_id
                        and e.lesson_type_id == first_entry.lesson_type_id
                        for e in lesson_entries
                    )
                    is_lecture = first_entry.lesson_type.name.lower() in [
                        "umumy",
                        "лекция",
                        "lecture",
                    ]

                    # determine if any entry for this lesson matches selected teacher
                    teacher_matches = False
                    if selected_teacher_id:
                        for e in lesson_entries:
                            if e.teacher_id and str(e.teacher_id) == str(
                                selected_teacher_id
                            ):
                                teacher_matches = True
                                break

                    if is_lecture and is_same_subject:
                        if selected_teacher_id and not teacher_matches:
                            # keep lecture row but blank content when teacher filter doesn't match
                            lesson_data[lesson_num_obj.number] = {
                                "is_lecture": True,
                                "subject": None,
                                "lesson_type": first_entry.lesson_type.name,
                                "teacher": None,
                                "room": None,
                                "groups": [e.group.name for e in lesson_entries],
                            }
                        else:
                            lesson_data[lesson_num_obj.number] = {
                                "is_lecture": True,
                                "subject": first_entry.subject.name,
                                "lesson_type": first_entry.lesson_type.name,
                                "teacher": first_entry.teacher.name
                                if first_entry.teacher
                                else None,
                                "room": first_entry.room or None,
                                "groups": [e.group.name for e in lesson_entries],
                            }
                    else:
                        # For practice sessions, list each group's lesson in the correct order
                        group_lessons_dict = {}
                        for e in lesson_entries:
                            group_lessons_dict[e.group.name] = {
                                "group": e.group.name,
                                "subject": e.subject.name,
                                "lesson_type": e.lesson_type.name,
                                "teacher": e.teacher.name if e.teacher else None,
                                "teacher_id": e.teacher_id,
                                "room": e.room or None,
                            }

                        # Build a map that contains an entry for each group in group_order
                        group_lessons_map = {}
                        if group_order:
                            for g in group_order:
                                gl = group_lessons_dict.get(g)
                                if (
                                    selected_teacher_id
                                    and gl
                                    and gl.get("teacher_id")
                                    and str(gl.get("teacher_id"))
                                    != str(selected_teacher_id)
                                ):
                                    group_lessons_map[g] = None
                                else:
                                    group_lessons_map[g] = gl
                        else:
                            for gname, glesson in group_lessons_dict.items():
                                if (
                                    selected_teacher_id
                                    and glesson
                                    and glesson.get("teacher_id")
                                    and str(glesson.get("teacher_id"))
                                    != str(selected_teacher_id)
                                ):
                                    group_lessons_map[gname] = None
                                else:
                                    group_lessons_map[gname] = glesson

                        lesson_data[lesson_num_obj.number] = {
                            "is_lecture": False,
                            "group_lessons": [
                                v for v in group_lessons_map.values() if v
                            ],
                            "group_lessons_map": group_lessons_map,
                        }
                if lesson_data:
                    timetable_data[day.id] = {
                        "day_name": day.get_number_display(),
                        "lessons": lesson_data,
                        "lesson_count": len(lesson_data),
                    }
            return timetable_data, lesson_number_objs

        # If no specific week selected or "ahli" (all weeks), show both weeks
        if not selected_week or selected_week == "ahli" or selected_week == "":
            # Для week1
            if week1_entries.exists():
                timetable_data, lesson_number_objs = build_timetable(
                    week1_entries, group_names, selected_teacher
                )
                if timetable_data:
                    week1_courses_data.append(
                        {
                            "course": course,
                            "groups": group_names,
                            "timetable": timetable_data,
                            "lesson_numbers": lesson_number_objs,
                            "week_numbers": [1],
                            "group_colspan": groups.count() * 2,
                        }
                    )
            # Для week2
            if week2_entries.exists():
                timetable_data, lesson_number_objs = build_timetable(
                    week2_entries, group_names, selected_teacher
                )
                if timetable_data:
                    week2_courses_data.append(
                        {
                            "course": course,
                            "groups": group_names,
                            "timetable": timetable_data,
                            "lesson_numbers": lesson_number_objs,
                            "week_numbers": [2],
                            "group_colspan": groups.count() * 2,
                        }
                    )
        else:
            # For a specific week
            if filtered_entries.exists():
                timetable_data, lesson_number_objs = build_timetable(
                    filtered_entries, group_names, selected_teacher
                )
                if timetable_data:
                    all_courses_data.append(
                        {
                            "course": course,
                            "groups": group_names,
                            "timetable": timetable_data,
                            "lesson_numbers": lesson_number_objs,
                            "week_numbers": [int(selected_week)]
                            if selected_week
                            else [],
                            "group_colspan": groups.count() * 2,
                        }
                    )

    context = {
        "faculties": faculties,
        "courses": courses,
        "teachers": teachers,
        "weeks": weeks,
        "days": days,
        "selected_faculty": selected_faculty,
        "selected_course": selected_course,
        "selected_teacher": selected_teacher,
        "selected_week": selected_week,
        "selected_day": selected_day,
        "selected_week_obj": selected_week_obj,
        "selected_day_obj": selected_day_obj,
        "week1_courses_data": week1_courses_data,
        "week2_courses_data": week2_courses_data,
        "courses_data": all_courses_data,
    }

    return render(request, "timetable_grid.html", context)
