from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Week, Day, TimetableEntry, Faculty, Course, Group, Teacher, LessonNumber
from .serializers import TimetableEntrySerializer
from .filters import TimetableEntryFilter



class WeekDayScheduleAPIView(APIView):
    def get(self, request, week_number, day_number):
        week = get_object_or_404(Week, number=week_number)

        day = Day.objects.filter(number=day_number).first()
        if not day:
            return Response(
                {"detail": "Day not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        lessons = TimetableEntry.objects.filter(
            week=week,
            day=day
        ).order_by('lesson_number__number')

        serializer = TimetableEntrySerializer(lessons, many=True)

        return Response({
            "week": week.number,
            "day_number": day.number,
            "day_name": day.get_number_display(),
            "schedule": serializer.data
        })
    


class WeekScheduleAPIView(APIView):
    def get(self, request, week_number):
        week = get_object_or_404(Week, number=week_number)

        lessons = TimetableEntry.objects.filter(
            week=week,
        ).order_by('lesson_number__number')

        serializer = TimetableEntrySerializer(lessons, many=True)

        return Response({
            "week": week.number,
            "schedule": serializer.data
        })

    
class TimetableSearchAPIView(ListAPIView):
    queryset = TimetableEntry.objects.select_related(
        'week', 'day', 'group', 'lesson_number', 'subject', 'teacher'
    ).all()
    serializer_class = TimetableEntrySerializer
    filterset_class = TimetableEntryFilter


# Frontend Views
def timetable_view(request):
    """Main timetable view with filters"""
    # Get all filter options
    faculties = Faculty.objects.all().order_by('name')
    courses = Course.objects.all().order_by('number')
    groups = Group.objects.all().order_by('name')
    teachers = Teacher.objects.all().order_by('name')
    weeks = Week.objects.all().order_by('number')
    days = Day.objects.all().order_by('number')
    
    # Get selected filters from request
    selected_faculty = request.GET.get('faculty', '')
    selected_course = request.GET.get('course', '')
    selected_group = request.GET.get('group', '')
    selected_teacher = request.GET.get('teacher', '')
    selected_week = request.GET.get('week', '')
    selected_day = request.GET.get('day', '')
    
    # Filter courses based on selected faculty
    if selected_faculty:
        courses = courses.filter(faculty_id=selected_faculty)
    
    # Filter groups based on selected course
    if selected_course:
        groups = groups.filter(course_id=selected_course)
    
    # Build query for timetable entries
    entries = TimetableEntry.objects.select_related(
        'week', 'day', 'group', 'group__course', 'group__course__faculty',
        'lesson_number', 'subject', 'teacher', 'lesson_type'
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
    
    # Order entries
    entries = entries.order_by('week__number', 'day__number', 'lesson_number__number')
    
    context = {
        'faculties': faculties,
        'courses': courses,
        'groups': groups,
        'teachers': teachers,
        'weeks': weeks,
        'days': days,
        'entries': entries,
        'selected_faculty': selected_faculty,
        'selected_course': selected_course,
        'selected_group': selected_group,
        'selected_teacher': selected_teacher,
        'selected_week': selected_week,
        'selected_day': selected_day,
    }
    
    return render(request, 'timetable.html', context)


def timetable_grid(request):
    """Grid view of timetable - Excel-like format with days as rows and lesson numbers as columns"""
    # Get all filter options
    faculties = Faculty.objects.all().order_by('name')
    weeks = Week.objects.all().order_by('number')
    days = Day.objects.all().order_by('number')
    
    # Get selected filters
    selected_faculty = request.GET.get('faculty', '')
    selected_course = request.GET.get('course', '')
    selected_week = request.GET.get('week', '')
    
    # Get courses for selected faculty or all
    courses = Course.objects.select_related('faculty').all().order_by('faculty__name', 'number')
    if selected_faculty:
        courses = courses.filter(faculty_id=selected_faculty)
    if selected_course:
        courses = courses.filter(id=selected_course)
    
    selected_week_obj = None
    if selected_week:
        selected_week_obj = Week.objects.get(id=selected_week)
    
    # Build timetable data for each course
    courses_data = []
    
    for course in courses:
        # Get all groups for this course
        groups = Group.objects.filter(course=course).order_by('name')
        
        if not groups.exists():
            continue
        
        group_names = [g.name for g in groups]
        
        # Build query for entries
        entries_query = TimetableEntry.objects.select_related(
            'week', 'day', 'group', 'lesson_number', 'subject', 'teacher', 'lesson_type'
        ).filter(group__course=course)
        
        if selected_week:
            entries_query = entries_query.filter(week_id=selected_week)
        
        entries = entries_query.order_by('day__number', 'lesson_number__number', 'group__name')
        
        if not entries.exists():
            continue
        
        # Get all lesson numbers that have entries
        lesson_numbers = entries.values_list('lesson_number', flat=True).distinct()
        lesson_number_objs = LessonNumber.objects.filter(id__in=lesson_numbers).order_by('number')
        
        # Debug output
        print(f"\n=== Course: {course.faculty.name} — {course.number} Kurs ===")
        print(f"Lesson number objects: {[ln.number for ln in lesson_number_objs]}")
        
        # Organize data: day -> lesson_number -> entries
        from collections import defaultdict
        timetable_data = {}
        
        for day in days:
            day_entries = entries.filter(day=day)
            
            if not day_entries.exists():
                continue
            
            lesson_data = {}
            
            print(f"  Day: {day.get_number_display()}")
            
            for lesson_num_obj in lesson_number_objs:
                lesson_entries = day_entries.filter(lesson_number=lesson_num_obj)
                
                print(f"    Lesson #{lesson_num_obj.number}: {lesson_entries.count()} entries")
                
                if lesson_entries.exists():
                    # Check if all entries have the same subject and lesson type
                    first_entry = lesson_entries.first()
                    is_same_subject = all(
                        e.subject_id == first_entry.subject_id and 
                        e.lesson_type_id == first_entry.lesson_type_id
                        for e in lesson_entries
                    )
                    
                    # If it's a lecture (umumy) - merge with same subject
                    is_lecture = first_entry.lesson_type.name.lower() in ['umumy', 'лекция', 'lecture']
                    
                    if is_lecture and is_same_subject:
                        # Merged cell for all groups (same subject lecture)
                        lesson_data[lesson_num_obj.number] = {
                            'is_lecture': True,
                            'subject': first_entry.subject.name,
                            'lesson_type': first_entry.lesson_type.name,
                            'teacher': first_entry.teacher.name if first_entry.teacher else None,
                            'room': first_entry.room or None,
                            'groups': [e.group.name for e in lesson_entries]
                        }
                        print(f"      -> Lecture: {first_entry.subject.name}")
                    else:
                        # Practice or different subjects - show all in one row with horizontal division
                        lesson_data[lesson_num_obj.number] = {
                            'is_lecture': False,
                            'group_lessons': [
                                {
                                    'group': e.group.name,
                                    'subject': e.subject.name,
                                    'lesson_type': e.lesson_type.name,
                                    'teacher': e.teacher.name if e.teacher else None,
                                    'room': e.room or None,
                                }
                                for e in lesson_entries
                            ]
                        }
                        print(f"      -> Practice with {len(lesson_entries)} groups: {[e.subject.name for e in lesson_entries]}")

            
            if lesson_data:
                timetable_data[day.id] = {
                    'day_name': day.get_number_display(),
                    'lessons': lesson_data,
                    'lesson_count': len(lesson_data)
                }
        
        if timetable_data:
            # Get weeks for this course
            course_weeks = entries.values_list('week__number', flat=True).distinct().order_by('week__number')
            week_numbers = list(course_weeks)
            
            print(f"\n  Передаем в шаблон lesson_numbers: {[ln.number for ln in lesson_number_objs]}")
            print(f"  Всего timetable_data дней: {len(timetable_data)}")
            for day_id, day_info in timetable_data.items():
                print(f"    День {day_info['day_name']}: ключи уроков = {list(day_info['lessons'].keys())}")
                for lesson_key, lesson_val in day_info['lessons'].items():
                    print(f"      Урок #{lesson_key}: is_lecture={lesson_val.get('is_lecture')}, group_lessons count={len(lesson_val.get('group_lessons', []))} or subject={lesson_val.get('subject')}")
            
            courses_data.append({
                'course': course,
                'groups': group_names,
                'lesson_numbers': lesson_number_objs,
                'timetable': timetable_data,
                'week_numbers': week_numbers
            })
    
    context = {
        'faculties': faculties,
        'weeks': weeks,
        'days': days,
        'selected_faculty': selected_faculty,
        'selected_course': selected_course,
        'selected_week': selected_week,
        'selected_week_obj': selected_week_obj,
        'courses_data': courses_data,
    }
    
    return render(request, 'timetable_grid.html', context)

