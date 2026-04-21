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
        ('beginner', "Boshlang'ich"),
        ('intermediate', "O'rta"),
        ('advanced', 'Yuqori'),
    ]
    LANGUAGE_CHOICES = [
        ('uz', "O'zbek tili"),
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
    video_url = models.URLField(blank=True)
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
    progress = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Ro'yxat"
        verbose_name_plural = "Ro'yxatlar"
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


# ============ TEST (QUIZ) MODELLARI ============

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200, verbose_name='Test nomi')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    time_limit_minutes = models.PositiveIntegerField(default=10, verbose_name='Vaqt (daqiqa, 0=cheksiz)')
    pass_percentage = models.PositiveIntegerField(default=60, verbose_name="O'tish foizi (%)")
    max_attempts = models.PositiveIntegerField(default=3, verbose_name='Max urinish (0=cheksiz)')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'

    def __str__(self):
        return f"{self.lesson.title} — {self.title}"

    def total_questions(self):
        return self.questions.count()

    def total_points(self):
        return sum(q.points for q in self.questions.all())


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Savol matni')
    points = models.PositiveIntegerField(default=1, verbose_name='Ball')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    explanation = models.TextField(blank=True, verbose_name='Izoh (javobdan keyin)')

    class Meta:
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} — {self.text[:60]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300, verbose_name='Javob varianti')
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Javob varianti'
        verbose_name_plural = 'Javob variantlari'
        ordering = ['order']

    def __str__(self):
        return f"{'OK' if self.is_correct else 'X'} {self.text[:50]}"


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0)
    is_passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Test urinishi'
        verbose_name_plural = 'Test urinishlari'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.username} — {self.quiz.title} ({self.percentage:.0f}%)"


class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Javob'
        verbose_name_plural = 'Javoblar'
