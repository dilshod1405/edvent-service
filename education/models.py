from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    profession = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
    
    def __str__(self):
        return self.name


class FoundationCourse(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='foundation_courses', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='foundation_courses/')
    price = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = 'Foundation Course'
        verbose_name_plural = 'Foundation Courses'
    
    def __str__(self):
        return self.title
    
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=255, unique=True)
    foundation_course = models.ForeignKey(
        FoundationCourse,
        related_name='videos',
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title


class Speciality(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'
    
    def __str__(self):
        return self.title


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='courses', on_delete=models.SET_NULL, null=True)
    speciality = models.ForeignKey(Speciality, related_name='courses', on_delete=models.CASCADE)
    support = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supported_courses'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='courses/')
    duration = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    
    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_id = models.CharField(max_length=255, unique=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    def __str__(self):
        return f'{self.module.course.title} - {self.module.title} - {self.title}'


class Tariff(models.Model):
    title = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    courses = models.ManyToManyField(Course, related_name='tariffs')
    discount_percent = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tariff'
        verbose_name_plural = 'Tariffs'
    
    def __str__(self):
        return self.title


class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    
    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
    
    def __str__(self):
        return f'{self.lesson.title} - {self.title}'


class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='homeworks', on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'
    
    def __str__(self):
        return f'{self.lesson.title}'
