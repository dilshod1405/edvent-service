from rest_framework import serializers
from .models import (
    Teacher, FoundationCourse, Video, Speciality,
    Course, Module, Lesson, Tariff, Resource, Homework
)

# Teacher
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'experience', 'profession', 'company', 'logo']


# Video (reverse relation from FoundationCourse)
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_url']


# FoundationCourse
class FoundationCourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = FoundationCourse
        fields = ['id', 'title', 'description', 'photo', 'price', 'teacher', 'videos']


# Speciality
class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'title', 'description']


# Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'duration']


# Module
class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'price', 'lessons']


# Course (with nested modules and teacher)
class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    speciality = SpecialitySerializer()
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'photo', 'duration', 'teacher', 'speciality', 'modules']


# Resource
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'file']


# Homework
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'description', 'file']


# Tariff (can be shown per speciality or course)
class TariffSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Tariff
        fields = ['id', 'title', 'price', 'discount_percent', 'is_active', 'speciality', 'courses']
