from django.contrib import admin
from .models import (
    Teacher, Speciality, Course, Module, Lesson,
    Resource, Homework, Tariff, Video
)


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1


class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'description', 'video_id', 'duration', 'id')
    search_fields = ('title', 'module__title')
    inlines = [ResourceInline, HomeworkInline]
    ordering = ('id',)
    list_editable = ('video_id', 'duration')
    list_filter = ('module',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'price', 'id')
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]
    ordering = ('id',)
    list_filter = ('course',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'speciality', 'teacher', 'duration', 'id')
    list_editable = ('duration',)
    ordering = ('id',)
    list_filter = ('speciality',)
    search_fields = ('title', 'description', 'teacher__name')
    inlines = [ModuleInline]



@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('title', 'speciality', 'price', 'discount_percent', 'is_active', 'id')
    list_filter = ('speciality', 'is_active')
    filter_horizontal = ('courses',)
    search_fields = ('title',)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'id')
    search_fields = ('title',)
    ordering = ('id',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('profession', 'company', 'id')
    list_editable = ('company', )
    ordering = ('id',)


from .models import FoundationCourse
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    
    
@admin.register(FoundationCourse)
class FoundationCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'video_count')
    search_fields = ('title', 'teacher__name')
    inlines = [VideoInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = Teacher.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videolar soni'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'foundation_course')
    search_fields = ('title', 'foundation_course__title')