from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class TimetableEntrySerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    lesson_number = serializers.StringRelatedField()
    lesson_type = serializers.StringRelatedField()
    day = serializers.StringRelatedField()
    week = serializers.StringRelatedField()


    class Meta:
        model = TimetableEntry
        fields = '__all__'