from rest_framework import serializers
from authentication.serializers.user_detail_serializer import UserDetailSerializer
from .models import (
    Teacher, FoundationCourse, Video, Speciality,
    Course, Module, Lesson, Tariff, Resource, Homework
)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'experience', 'profession', 'company', 'logo']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_id']

class FoundationCourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = FoundationCourse
        fields = ['id', 'title', 'description', 'photo', 'price', 'teacher', 'videos']




# Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_id', 'duration']
        
        
# Module
class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'price', 'lessons']


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


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'photo', 'duration']


class SpecialitySerializer(serializers.ModelSerializer):
    courses = CourseShortSerializer(many=True, read_only=True)

    class Meta:
        model = Speciality
        fields = ['id', 'title', 'description', 'courses']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    speciality = SpecialitySerializer()
    modules = ModuleSerializer(many=True, read_only=True)
    support = UserDetailSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'photo', 'duration', 'teacher', 'support', 'speciality', 'modules']


# Tariff (can be shown per speciality or course)
class TariffSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Tariff
        fields = ['id', 'title', 'price', 'discount_percent', 'is_active', 'speciality', 'courses']


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']
        
        
class LessonDetailSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.id')
    module_title = serializers.CharField(source='module.title')
    course_id = serializers.IntegerField(source='module.course.id')
    course_title = serializers.CharField(source='module.course.title')
    
    resources = ResourceSerializer(many=True, read_only=True)
    homeworks = HomeworkSerializer(many=True, read_only=True)
    
    module_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'video_id', 'duration',
            'module_id', 'module_title',
            'course_id', 'course_title',
            'resources', 'homeworks',
            'module_lessons',
        ]
    
    def get_module_lessons(self, obj):
        lessons = Lesson.objects.filter(module=obj.module).exclude(id=obj.id)
        return LessonListSerializer(lessons, many=True).data