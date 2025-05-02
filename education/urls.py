from django.urls import path
from .views import (
    FoundationCourseListAPIView,
    CourseListAPIView,
    CourseDetailAPIView,
    FoundationCourseDetailAPIView,
    HomeworkListByLessonAPIView,
    ResourceListByLessonAPIView,
    TeacherListAPIView,
    TariffListAPIView,
    TariffDetailAPIView,
    SpecialityListAPIView,
    SpecialityDetailAPIView
)

urlpatterns = [
    path('foundation-courses/', FoundationCourseListAPIView.as_view(), name='foundation-course-list'),
    path('foundation-courses/<int:id>/', FoundationCourseDetailAPIView.as_view(), name='foundation-course-detail'),
    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('teachers/', TeacherListAPIView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherListAPIView.as_view(), name='teacher-detail'),
    path('tariffs/', TariffListAPIView.as_view(), name='tariff-list'),
    path('tariffs/<int:pk>/', TariffDetailAPIView.as_view(), name='tariff-detail'),
    path('specialities/', SpecialityListAPIView.as_view(), name='speciality-list'),
    path('specialities/<int:pk>/', SpecialityDetailAPIView.as_view(), name='speciality-detail'),
    path('homework/<int:lesson_id>/', HomeworkListByLessonAPIView.as_view(), name='homework-by-lesson'),
    path('resource/<int:lesson_id>/', ResourceListByLessonAPIView.as_view(), name='resource-by-lesson'),
]
