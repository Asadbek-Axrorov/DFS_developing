from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Course, Module, Lesson, Enrollment, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon_name', 'name', 'slug', 'courses_count')
    prepopulated_fields = {'slug': ('name',)}

    def icon_name(self, obj):
        return format_html('<span style="font-size:20px;">{}</span> {}', obj.icon, obj.name)
    icon_name.short_description = 'Kategoriya'

    def courses_count(self, obj):
        count = obj.courses.count()
        return format_html('<span style="background:#EEF2FF;color:#4F46E5;padding:3px 10px;border-radius:20px;font-weight:600;">{} kurs</span>', count)
    courses_count.short_description = 'Kurslar'


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'category', 'mentor_info', 'curator_info', 'level_badge', 'students_badge', 'rating_stars', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'level', 'language', 'category')
    search_fields = ('title', 'description', 'mentor__username')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
    inlines = [ModuleInline]
    list_per_page = 15
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'short_description', 'description', 'thumbnail', 'category'),
        }),
        ('O\'qituvchi va Kurator', {
            'fields': ('mentor', 'curator'),
        }),
        ('Parametrlar', {
            'fields': ('level', 'language', 'duration_hours', 'price', 'is_free'),
            'classes': ('wide',),
        }),
        ('Holat', {
            'fields': ('is_published', 'is_featured', 'students_count', 'rating'),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="35" style="border-radius:6px; object-fit:cover;"/>', obj.thumbnail.url)
        colors = {'beginner': '#4F46E5', 'intermediate': '#059669', 'advanced': '#DC2626'}
        color = colors.get(obj.level, '#6B7280')
        return format_html(
            '<div style="width:50px;height:35px;background:{};border-radius:6px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">📚</div>',
            color
        )
    thumbnail_preview.short_description = ''

    def mentor_info(self, obj):
        if obj.mentor:
            return format_html('<span style="color:#059669;font-weight:600;">👨‍🏫 {}</span>', obj.mentor.get_full_name() or obj.mentor.username)
        return format_html('<span style="color:#9CA3AF;">—</span>')
    mentor_info.short_description = 'Mentor'

    def curator_info(self, obj):
        if obj.curator:
            return format_html('<span style="color:#D97706;font-weight:600;">🎯 {}</span>', obj.curator.get_full_name() or obj.curator.username)
        return format_html('<span style="color:#9CA3AF;">—</span>')
    curator_info.short_description = 'Kurator'

    def level_badge(self, obj):
        colors = {
            'beginner': ('#EEF2FF', '#4F46E5', '🌱'),
            'intermediate': ('#ECFDF5', '#059669', '🚀'),
            'advanced': ('#FEF2F2', '#DC2626', '⚡'),
        }
        bg, color, icon = colors.get(obj.level, ('#F3F4F6', '#6B7280', '📚'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 8px;border-radius:20px;font-size:11px;font-weight:600;">{} {}</span>',
            bg, color, icon, obj.get_level_display()
        )
    level_badge.short_description = 'Daraja'

    def students_badge(self, obj):
        return format_html('<span style="font-weight:600;">👥 {}</span>', obj.students_count)
    students_badge.short_description = 'Talabalar'

    def rating_stars(self, obj):
        stars = '★' * int(obj.rating) + '☆' * (5 - int(obj.rating))
        return format_html('<span style="color:#F59E0B;font-size:14px;">{}</span> <span style="color:#6B7280;font-size:11px;">{}</span>', stars, obj.rating)
    rating_stars.short_description = 'Reyting'


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    fields = ('title', 'lesson_type', 'video_url', 'video_file', 'duration_minutes', 'order', 'is_free_preview')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'lessons_count')
    list_filter = ('course',)
    inlines = [LessonInline]

    def lessons_count(self, obj):
        count = obj.lessons.count()
        return format_html('<span style="background:#ECFDF5;color:#059669;padding:3px 10px;border-radius:20px;font-weight:600;">{} dars</span>', count)
    lessons_count.short_description = 'Darslar'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'type_badge', 'duration_minutes', 'is_free_preview')
    list_filter = ('lesson_type', 'is_free_preview', 'module__course')
    search_fields = ('title',)

    def type_badge(self, obj):
        icons = {'video': ('🎬', '#4F46E5', '#EEF2FF'), 'text': ('📝', '#059669', '#ECFDF5'), 'quiz': ('❓', '#D97706', '#FFFBEB'), 'task': ('✅', '#DC2626', '#FEF2F2')}
        icon, color, bg = icons.get(obj.lesson_type, ('📚', '#6B7280', '#F3F4F6'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 8px;border-radius:20px;font-size:11px;font-weight:600;">{} {}</span>',
            bg, color, icon, obj.get_lesson_type_display()
        )
    type_badge.short_description = 'Tur'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress_bar', 'is_completed', 'enrolled_at')
    list_filter = ('is_completed', 'course')
    search_fields = ('student__username', 'course__title')

    def progress_bar(self, obj):
        color = '#059669' if obj.progress >= 80 else '#4F46E5' if obj.progress >= 40 else '#F59E0B'
        return format_html(
            '<div style="width:120px;background:#F3F4F6;border-radius:10px;height:8px;">'
            '<div style="width:{}%;background:{};border-radius:10px;height:8px;"></div>'
            '</div> <span style="font-size:11px;color:#6B7280;">{}%</span>',
            obj.progress, color, obj.progress
        )
    progress_bar.short_description = 'Progress'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'star_rating', 'comment_short', 'created_at')
    list_filter = ('rating', 'course')

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#F59E0B;">{}</span>', stars)
    star_rating.short_description = 'Reyting'

    def comment_short(self, obj):
        return obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
    comment_short.short_description = 'Sharh'
