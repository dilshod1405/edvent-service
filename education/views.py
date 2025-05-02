from rest_framework import generics
from .models import FoundationCourse, Course, Speciality, Teacher, Tariff, Homework, Resource
from .serializers import FoundationCourseSerializer, CourseSerializer, SpecialitySerializer, TeacherSerializer, TariffSerializer, HomeworkSerializer, ResourceSerializer
from rest_framework.generics import RetrieveAPIView

class FoundationCourseListAPIView(generics.ListAPIView):
    queryset = FoundationCourse.objects.select_related('teacher').prefetch_related('videos').all()
    serializer_class = FoundationCourseSerializer


class FoundationCourseDetailAPIView(RetrieveAPIView):
    queryset = FoundationCourse.objects.all()
    serializer_class = FoundationCourseSerializer
    lookup_field = 'id'
    
    

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.select_related('teacher', 'speciality').prefetch_related('modules__lessons').all()
    serializer_class = CourseSerializer


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.select_related('teacher', 'speciality').prefetch_related('modules__lessons').all()
    serializer_class = CourseSerializer


class SpecialityListAPIView(generics.ListAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialityDetailAPIView(generics.RetrieveAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class TeacherListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetailAPIView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.select_related('speciality').prefetch_related('courses').all()
    serializer_class = TariffSerializer


class TariffDetailAPIView(generics.RetrieveAPIView):
    queryset = Tariff.objects.select_related('speciality').prefetch_related('courses').all()
    serializer_class = TariffSerializer


class HomeworkListByLessonAPIView(generics.ListAPIView):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return Homework.objects.filter(lesson_id=lesson_id)


class ResourceListByLessonAPIView(generics.ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return Resource.objects.filter(lesson_id=lesson_id)