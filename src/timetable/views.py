from django.shortcuts import render
from .models import Schedule, Week, Day, Teacher, Group, Faculty, Course
from django.utils import timezone

def timetable_view(request):
    # Получаем все данные
    faculties = Faculty.objects.all()
    courses = Course.objects.all()
    weeks = Week.objects.all()
    days = Day.objects.all()
    teachers = Teacher.objects.all()

    # Получаем текущий факультет и курс из GET-параметров или по умолчанию
    selected_faculty_id = request.GET.get('faculty', 'all')
    selected_course_id = request.GET.get('course', 'all')
    selected_week_id = request.GET.get('week', 'all')
    selected_day_id = request.GET.get('day', 'all')
    selected_teacher_id = request.GET.get('teacher')

    # Фильтрация групп по факультету и курсу
    groups = Group.objects.all()
    if selected_faculty_id != 'all':
        groups = groups.filter(course__faculty_id=selected_faculty_id)
    if selected_course_id != 'all':
        groups = groups.filter(course_id=selected_course_id)
    groups = groups.filter(course__number=1)[:2]  # Ограничиваем до двух групп (II Topar, III Topar)

    current_date = timezone.now()  # 16 октября 2025, 17:02 +05
    current_day_name = current_date.strftime('%A').lower()  # 'thursday' (Penşenbe)

    # Базовый запрос расписания
    schedules = Schedule.objects.select_related('lesson_number', 'group', 'day', 'week', 'teacher', 'subject', 'room')
    print(f"Total schedules in DB: {Schedule.objects.count()}")
    print(f"Loaded schedules: {schedules.count()}")

    # Фильтры
    if selected_week_id != 'all':
        schedules = schedules.filter(week_id=selected_week_id)
        print(f"After week filter {selected_week_id}: {schedules.count()} records")
    if selected_day_id != 'all':
        schedules = schedules.filter(day_id=selected_day_id)
        print(f"After day filter {selected_day_id}: {schedules.count()} records")
    if selected_teacher_id:
        schedules = schedules.filter(teacher_id=selected_teacher_id)
        print(f"After teacher filter {selected_teacher_id}: {schedules.count()} records")
    if selected_faculty_id != 'all' or selected_course_id != 'all':
        schedules = schedules.filter(group__course__faculty_id=selected_faculty_id if selected_faculty_id != 'all' else None,
                                     group__course_id=selected_course_id if selected_course_id != 'all' else None)
        print(f"After faculty/course filter: {schedules.count()} records")

    # Группировка по дням и парам
    grouped_schedules = {}
    for day in days:
        day_schedules = schedules.filter(day=day).order_by('lesson_number__pair_number')
        if day_schedules.exists():
            print(f"Day {day.name} has {day_schedules.count()} schedules")
        for schedule in day_schedules:
            day_name = day.name.lower()
            if day_name not in grouped_schedules:
                grouped_schedules[day_name] = {}
            pair_key = schedule.lesson_number.pair_number
            if pair_key not in grouped_schedules[day_name]:
                grouped_schedules[day_name][pair_key] = {'group1': None, 'group2': None}
            if schedule.group.name == groups[0].name:
                grouped_schedules[day_name][pair_key]['group1'] = schedule
            elif schedule.group.name == groups[1].name:
                grouped_schedules[day_name][pair_key]['group2'] = schedule

    print(f"Grouped schedules keys: {list(grouped_schedules.keys())}")
    context = {
        'faculties': faculties,
        'courses': courses,
        'weeks': weeks,
        'days': days,
        'teachers': teachers,
        'groups': groups,
        'selected_faculty_id': selected_faculty_id,
        'selected_course_id': selected_course_id,
        'selected_week_id': selected_week_id,
        'selected_day_id': selected_day_id,
        'selected_teacher_id': selected_teacher_id,
        'grouped_schedules': grouped_schedules,
        'current_day_name': current_day_name,
    }
    return render(request, 'timetable/timetable.html', context)