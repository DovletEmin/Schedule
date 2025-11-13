from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self): return self.name


class Course(models.Model):
    number = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')

    class Meta: unique_together = (('number', 'faculty'),)
    
    def __str__(self): return f"{self.faculty.name} — {self.number} курс"


class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    
    class Meta: unique_together = (('name', 'course'),)
    
    def __str__(self): return f"{self.course} / {self.name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self): return f"{self.last_name} {self.first_name}"


class Week(models.Model):
    name = models.CharField(max_length=50, help_text='Чётная / Нечётная или 1 неделя')

    def __str__(self): return self.name


class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta: ordering = ['order']
    
    def __str__(self): return self.name


class LessonNumber(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
   
    def __str__(self): return str(self.number)


class LessonType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self): return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self): return self.name


class TimetableEntry(models.Model):
    week = models.ForeignKey(Week, on_delete=models.PROTECT)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson_number = models.ForeignKey(LessonNumber, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    lesson_type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    room = models.CharField(max_length=50, blank=True)


    class Meta:
        unique_together = (('week', 'day', 'group', 'lesson_number'),)
        ordering = ['week__id', 'day__order', 'lesson_number__number']


    def __str__(self):
        return f"{self.group} | {self.week} | {self.day} #{self.lesson_number} — {self.subject}"