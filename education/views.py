from rest_framework import generics
from .models import FoundationCourse, Course, Speciality, Teacher, Tariff, Homework, Resource, Lesson
from .serializers import FoundationCourseSerializer, CourseSerializer, SpecialitySerializer, TeacherSerializer, TariffSerializer, HomeworkSerializer, ResourceSerializer
from rest_framework.generics import RetrieveAPIView
from authentication.serializers.user_detail_serializer import UserDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests
from rest_framework.generics import ListAPIView
from .serializers import LessonSerializer

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


class LessonSupportAPIView(APIView):
    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.select_related('module__course__support').get(id=lesson_id)
            support = lesson.module.course.support
            serializer = UserDetailSerializer(support, context={'request': request})
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)


class ModuleLessonsView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        module_id = self.kwargs['module_id']
        return Lesson.objects.filter(module_id=module_id).order_by('id')


# VdoCipher OTP view
class VdoCipherOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)

        video_id = lesson.video_id

        api_url = f"https://dev.vdocipher.com/api/videos/{video_id}/otp"
        headers = {
            "Authorization": f"Apisecret {settings.VDOCIPHER_API_SECRET}",
            "Content-Type": "application/json",
        }

        payload = {
            "ttl": 300,  # URL 5 daqiqa amal qiladi
            "annotate": [
                {
                    "text": request.user.username,
                    "color": "white",
                    "alpha": 0.5,
                    "size": "14",
                    "interval": 5000,
                    "duration": 1000,
                    "position": "random"
                },
                {
                    "text": request.user.get_full_name(),
                    "color": "white",
                    "alpha": 0.5,
                    "size": "16",
                    "position": "bottom-right"
                }
            ]
        }

        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response(
                {"error": "Failed to get OTP", "details": response.json()},
                status=response.status_code
            )