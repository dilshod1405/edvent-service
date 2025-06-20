from django.urls import path
from .views import (
    FoundationCourseListAPIView,
    FoundationCourseDetailAPIView,
    CourseListAPIView,
    CourseDetailAPIView,
    ModuleLessonsView,
    TeacherListAPIView,
    TeacherDetailAPIView,
    TariffListAPIView,
    TariffDetailAPIView,
    SpecialityAPIView,
    LessonSupportAPIView,
    VdoCipherOTPView,
    LessonDetailView,
    HomeworkListByLessonAPIView,
    ResourceListByLessonAPIView,
    PaidCoursesView,
)

urlpatterns = [
    path('foundation-courses/', FoundationCourseListAPIView.as_view(), name='foundation-course-list'),
    path('foundation-courses/<int:pk>/', FoundationCourseDetailAPIView.as_view(), name='foundation-course-detail'),

    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),

    path('modules/<int:module_id>/lessons/', ModuleLessonsView.as_view(), name='module-lessons'),

    path('teachers/', TeacherListAPIView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetailAPIView.as_view(), name='teacher-detail'),

    path('tariffs/', TariffListAPIView.as_view(), name='tariff-list'),
    path('tariffs/<int:pk>/', TariffDetailAPIView.as_view(), name='tariff-detail'),

    path('specialities/', SpecialityAPIView.as_view(), name='speciality-list'),
    path('specialities/<int:pk>/', SpecialityAPIView.as_view(), name='speciality-detail'),

    path('lessons/<int:lesson_id>/support/', LessonSupportAPIView.as_view(), name='lesson-support'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    path('homework/<int:lesson_id>/', HomeworkListByLessonAPIView.as_view(), name='homework-by-lesson'),
    path('resource/<int:lesson_id>/', ResourceListByLessonAPIView.as_view(), name='resource-by-lesson'),

    path('vdocipher/otp/<str:video_id>/', VdoCipherOTPView.as_view(), name='vdocipher-otp'),

    path('user/paid-courses/', PaidCoursesView.as_view(), name='user-paid-courses'),
]
