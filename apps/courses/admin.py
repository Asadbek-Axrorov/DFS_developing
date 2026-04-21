from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Course, Module, Lesson,
    Enrollment, LessonProgress, Review,
    Quiz, Question, Choice, QuizAttempt, QuizAnswer
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('title', 'order')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'category', 'level', 'is_published', 'is_featured', 'students_count')
    list_filter = ('is_published', 'is_featured', 'level', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
    inlines = [ModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'lesson_type', 'order', 'is_free_preview')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'duration_minutes', 'is_free_preview', 'order')
    list_filter = ('lesson_type', 'is_free_preview')
    search_fields = ('title',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'progress', 'is_completed')
    list_filter = ('is_completed',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    list_filter = ('rating',)


# ============ TEST (QUIZ) ADMIN ============

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    max_num = 4
    fields = ('text', 'is_correct', 'order')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ('text', 'points', 'order', 'explanation')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'questions_count', 'time_limit_minutes', 'pass_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'lesson__title')
    list_editable = ('is_active',)
    inlines = [QuestionInline]
    fieldsets = (
        ('Asosiy', {
            'fields': ('lesson', 'title', 'description', 'is_active'),
        }),
        ('Sozlamalar', {
            'fields': ('time_limit_minutes', 'pass_percentage', 'max_attempts'),
        }),
    )

    def questions_count(self, obj):
        return format_html(
            '<b>{} savol / {} ball</b>',
            obj.questions.count(),
            obj.total_points()
        )
    questions_count.short_description = 'Savollar'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'quiz', 'points', 'order', 'correct_answer')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [ChoiceInline]

    def text_short(self, obj):
        t = obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
        return format_html('<b>{}</b>', t)
    text_short.short_description = 'Savol'

    def correct_answer(self, obj):
        correct = obj.choices.filter(is_correct=True).first()
        if correct:
            return format_html(
                '<span style="color:green;font-weight:bold;">{}</span>',
                correct.text[:50]
            )
        return format_html('<span style="color:red;">Belgilanmagan</span>')
    correct_answer.short_description = "To'g'ri javob"


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'total_points', 'percentage_display', 'passed_badge', 'started_at')
    list_filter = ('is_passed',)
    readonly_fields = ('student', 'quiz', 'score', 'total_points', 'percentage', 'is_passed', 'started_at', 'finished_at')

    def percentage_display(self, obj):
        color = 'green' if obj.percentage >= 60 else 'red'
        return format_html('<b style="color:{};">{}%</b>', color, int(obj.percentage))
    percentage_display.short_description = 'Natija'

    def passed_badge(self, obj):
        if obj.is_passed:
            return format_html('<span style="color:green;font-weight:bold;">O\'tdi</span>')
        return format_html('<span style="color:red;font-weight:bold;">O\'tmadi</span>')
    passed_badge.short_description = 'Holat'
