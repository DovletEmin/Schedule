from rest_framework import serializers
from .models import (
    Faculty, Course, Group, Teacher, Week, Day,
    LessonNumber, LessonType, Subject, TimetableEntry
)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class LessonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonNumber
        fields = ['id', 'number', 'start_time', 'end_time']


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'course']


class TimetableEntrySerializer(serializers.ModelSerializer):
    lesson_number = LessonNumberSerializer()
    subject = SubjectSerializer()
    teacher = TeacherSerializer()
    lesson_type = LessonTypeSerializer()
    group = GroupSerializer()

    class Meta:
        model = TimetableEntry
        fields = [
            'id',
            'lesson_number',
            'subject',
            'lesson_type',
            'teacher',
            'group',
            'room'
        ]


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name', 'order']


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'number']


class DayScheduleSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    day = serializers.CharField()
    schedule = TimetableEntrySerializer(many=True)