from django.db import models
from django.utils.translation import gettext_lazy as _


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    number = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty} {self.number}"
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.course}"
    
class Teacher(models.Model):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class Week(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class LessonNumber(models.Model):
    pair_number = models.CharField(max_length=5, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.pair_number} - ({self.start_time} - {self.end_time})"
    
class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    class LessonTypeChoices(models.TextChoices):
        LECTURE = 'LEC', _("Umumy")
        PRACTICE = 'PRA', _('Amaly')

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)  
    week = models.ForeignKey(Week, on_delete=models.PROTECT)
    lesson_number = models.ForeignKey(LessonNumber, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=3, choices=LessonTypeChoices.choices)

    class Meta:
        unique_together = ['group', 'day', 'week', 'lesson_number']

    def __str__(self):
        return f"{self.group} - {self.day} - {self.lesson_number} - {self.subject} - ({self.room})"