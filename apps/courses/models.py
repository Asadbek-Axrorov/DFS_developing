from django.db import models
from apps.accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='📚')
    color = models.CharField(max_length=20, default='#4F46E5')

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
    ]
    LANGUAGE_CHOICES = [
        ('uz', 'O\'zbek tili'),
        ('ru', 'Rus tili'),
        ('en', 'Ingliz tili'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teaching_courses', limit_choices_to={'role': 'mentor'})
    curator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='curating_courses', limit_choices_to={'role': 'curator'})
    thumbnail = models.FileField(upload_to='courses/thumbnails/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='uz')
    duration_hours = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    students_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Modul'
        verbose_name_plural = 'Modullar'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    LESSON_TYPE = [
        ('video', 'Video dars'),
        ('text', 'Matn dars'),
        ('quiz', 'Test'),
        ('task', 'Vazifa'),
    ]
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE, default='video')
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)  # YouTube yoki boshqa URL
    video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)  # percent

    class Meta:
        verbose_name = 'Ro\'yxat'
        verbose_name_plural = 'Ro\'yxatlar'
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'lesson')


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sharh'
        verbose_name_plural = 'Sharhlar'
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.rating}★)"
