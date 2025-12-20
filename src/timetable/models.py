from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Fakultet"

    def __str__(self):
        return self.name


class Course(models.Model):
    number = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="courses"
    )

    class Meta:
        unique_together = (("number", "faculty"),)
        verbose_name_plural = "Kurs"

    def __str__(self):
        return f"{self.faculty.name} — {self.number} Kurs"


class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")

    class Meta:
        unique_together = (("name", "course"),)
        verbose_name_plural = "Topar"

    def __str__(self):
        return f"{self.course} / {self.name}"


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Mugallym"

    def __str__(self):
        return self.name


class Week(models.Model):
    number = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name_plural = "Hepde"

    def __str__(self):
        return f"{str(self.number)} - Hepde"


class DayChoices(models.IntegerChoices):
    MON = 1, "Duşenbe"
    TUE = 2, "Sişenbe"
    WED = 3, "Çarşenbe"
    THU = 4, "Penşenbe"
    FRI = 5, "Anna"
    SAT = 6, "Şenbe"
    SUN = 7, "Ýekşenbe"


class Day(models.Model):
    number = models.PositiveSmallIntegerField(choices=DayChoices.choices, unique=True)

    class Meta:
        ordering = ["number"]
        verbose_name_plural = "Gün"

    def __str__(self):
        return self.get_number_display()


class LessonNumber(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sapak nomer"

    def __str__(self):
        return str(self.number)


class LessonType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Sapak görnüşi"

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Sapaklaryň ady"

    def __str__(self):
        return self.name


class TimetableEntry(models.Model):
    week = models.ForeignKey(Week, on_delete=models.PROTECT)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson_number = models.ForeignKey(LessonNumber, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(
        Teacher, blank=True, related_name="timetable_entries"
    )
    lesson_type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    room = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = (("week", "day", "group", "lesson_number"),)
        ordering = ["week__number", "day__number", "lesson_number__number"]
        verbose_name_plural = "Sapak tertibi"

    def __str__(self):
        return f"{self.group} | Week {self.week} | {self.day} #{self.lesson_number} — {self.subject}"
