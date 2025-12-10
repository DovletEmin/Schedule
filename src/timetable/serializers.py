from rest_framework import serializers
from .models import (
    Week,
    Day,
    Group,
    LessonNumber,
    LessonType,
    Subject,
    Teacher,
    TimetableEntry,
)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["name"]
        # fields = ['id', 'name']


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ["name"]
        # fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]
        # fields = ['id', 'name']


class LessonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonNumber
        fields = ["number"]
        # fields = ['id', 'number', 'start_time', 'end_time']


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ["course"]
        # fields = ['id', 'name', 'course']


class DaySerializer(serializers.ModelSerializer):
    number_display = serializers.CharField(source="get_number_display", read_only=True)

    class Meta:
        model = Day
        fields = ["number_display"]
        # fields = ['id', 'number', 'number_display']
        read_only_fields = ["number_display"]


class TimetableEntrySerializer(serializers.ModelSerializer):
    # week = serializers.StringRelatedField()
    # day = DaySerializer()
    group = serializers.StringRelatedField()
    # lesson_number = serializers.StringRelatedField()
    lesson_type = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = TimetableEntry
        fields = "__all__"
        # fields = ['group', 'lesson_type', 'subject', 'teacher']


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ["number"]
        # fields = ['id', 'number']


class DayScheduleSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    day = serializers.CharField()
    schedule = TimetableEntrySerializer(many=True)
