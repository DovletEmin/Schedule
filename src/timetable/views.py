from django.shortcuts import render
from .models import Schedule, Week, Day, Teacher, Group
from django.db.models import Q

def timetable_view(request):
    weeks = Week.objects.all()
    days = Day.objects.all()
    teachers = Teacher.objects.all()
    groups = Group.objects.filter(course__number=1)[:2]  

    selected_week_id = request.GET.get('week')
    selected_day_id = request.GET.get('day')
    selected_teacher_id = request.GET.get('teacher')

    schedules = Schedule.objects.all()

    if selected_week_id and selected_week_id != 'all':
        schedules = schedules.filter(week_id=selected_week_id)

    if selected_day_id and selected_day_id != 'all':
        schedules = schedules.filter(day_id=selected_day_id)

    if selected_teacher_id:
        schedules = schedules.filter(teacher_id=selected_teacher_id)

    grouped_schedules = {}
    for day in days:
        day_schedules = schedules.filter(day=day).order_by('lesson_number__number')
        for schedule in day_schedules:
            if day.name not in grouped_schedules:
                grouped_schedules[day.name] = {}
            lesson_num = schedule.lesson_number.number
            pair_key = f"{lesson_num}-{lesson_num+1}" if lesson_num % 2 == 1 else None  
            if pair_key:  
                if pair_key not in grouped_schedules[day.name]:
                    grouped_schedules[day.name][pair_key] = []
                grouped_schedules[day.name][pair_key].append(schedule)

    context = {
        'weeks': weeks,
        'days': days,
        'teachers': teachers,  
        'groups': groups,  
        'selected_week_id': selected_week_id or 'all',
        'selected_day_id': selected_day_id or 'all',
        'selected_teacher_id': selected_teacher_id,
        'grouped_schedules': grouped_schedules,
    }
    return render(request, 'timetable/timetable.html', context)