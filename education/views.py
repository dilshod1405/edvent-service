from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import (
    FoundationCourse, Course, Speciality, Teacher, Tariff, Homework,
    Resource, Lesson
)
from .serializers import (
    FoundationCourseSerializer, CourseSerializer, SpecialitySerializer,
    TeacherSerializer, TariffSerializer, HomeworkSerializer,
    ResourceSerializer, LessonSerializer, LessonDetailSerializer,
    UserDetailSerializer
)
import json
import requests
from django.db.models import Q
from rest_framework import permissions
from payment.models import Transaction


# === Foundation Courses ===
class FoundationCourseListAPIView(generics.ListAPIView):
    queryset = FoundationCourse.objects.select_related('teacher').prefetch_related('videos')
    serializer_class = FoundationCourseSerializer


class FoundationCourseDetailAPIView(generics.RetrieveAPIView):
    queryset = FoundationCourse.objects.select_related('teacher').prefetch_related('videos')
    serializer_class = FoundationCourseSerializer


# === Courses ===
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.select_related('teacher', 'speciality', 'support').prefetch_related('modules__lessons')
    serializer_class = CourseSerializer


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.select_related('teacher', 'speciality', 'support').prefetch_related('modules__lessons')
    serializer_class = CourseSerializer


# === Speciality (List & Retrieve) ===
class SpecialityAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            speciality = get_object_or_404(Speciality.objects.prefetch_related('courses'), pk=pk)
            serializer = SpecialitySerializer(speciality)
            return Response(serializer.data)
        queryset = Speciality.objects.prefetch_related('courses')
        serializer = SpecialitySerializer(queryset, many=True)
        return Response(serializer.data)


# === Teachers ===
class TeacherListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetailAPIView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


# === Tariffs ===
class TariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.select_related('speciality').prefetch_related('courses')
    serializer_class = TariffSerializer


class TariffDetailAPIView(generics.RetrieveAPIView):
    queryset = Tariff.objects.select_related('speciality').prefetch_related('courses')
    serializer_class = TariffSerializer


# === Lesson Detail ===
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.select_related('module__course').prefetch_related('resources', 'homeworks')
    serializer_class = LessonDetailSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        module_lessons_qs = Lesson.objects.filter(module=instance.module).values('id', 'title', 'duration').order_by('id')
        module_lessons = list(module_lessons_qs)
        data['module_lessons'] = module_lessons
        return Response(data, status=status.HTTP_200_OK)


class LessonSupportAPIView(APIView):
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson.objects.select_related('module__course__support'), id=lesson_id)
        support = lesson.module.course.support
        serializer = UserDetailSerializer(support, context={'request': request})
        return Response(serializer.data)


# === Lesson Resources & Homeworks ===
class HomeworkListByLessonAPIView(generics.ListAPIView):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        return Homework.objects.filter(lesson_id=self.kwargs['lesson_id'])


class ResourceListByLessonAPIView(generics.ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        return Resource.objects.filter(lesson_id=self.kwargs['lesson_id'])


# === Module Lessons ===
class ModuleLessonsView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(module_id=self.kwargs['module_id']).order_by('id')


# === VdoCipher OTP View ===
class VdoCipherOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        lesson = get_object_or_404(Lesson, video_id=video_id)
        api_url = f"https://dev.vdocipher.com/api/videos/{video_id}/otp"
        headers = {
            "Authorization": f"Apisecret {settings.VDOCIPHER_API_SECRET}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        annotate_string = json.dumps([
            {
                "type": "rtext",
                "text": request.user.username,
                "alpha": "0.60",
                "color": "0xFFFFFF",
                "size": "15",
                "interval": "5000"
            }
        ])
        payload = {
            "ttl": 300,
            "type": "video",
            "annotate": annotate_string
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Failed to get OTP", "details": response.json()}, status=response.status_code)


# === Get Paid Courses ===
class PaidCoursesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        # To‘langan modullar orqali kurs ID larni olish
        paid_course_ids_from_modules = Transaction.objects.filter(
            user=user,
            state='paid',
            module__isnull=False,
        ).values_list('module__course_id', flat=True)

        # To‘lov qilingan kurslar (agar bevosita kurs bo‘yicha bo‘lsa)
        paid_course_ids_direct = Transaction.objects.filter(
            user=user,
            state='paid',
            course__isnull=False,
        ).values_list('course_id', flat=True)

        # Ikkisini birlashtiramiz va takrorlarni olib tashlaymiz
        paid_course_ids = set(list(paid_course_ids_from_modules) + list(paid_course_ids_direct))

        # Kurslarni filterlaymiz
        return Course.objects.filter(id__in=paid_course_ids).distinct()