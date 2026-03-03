from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Category, Enrollment, Review, Lesson, LessonProgress
from apps.accounts.models import User


def home(request):
    featured_courses = Course.objects.filter(is_published=True, is_featured=True)[:6]
    all_courses = Course.objects.filter(is_published=True)[:12]
    categories = Category.objects.all()
    stats = {
        'courses': Course.objects.filter(is_published=True).count(),
        'students': User.objects.filter(role='student').count(),
        'mentors': User.objects.filter(role='mentor').count(),
    }
    return render(request, 'home.html', {
        'featured_courses': featured_courses,
        'all_courses': all_courses,
        'categories': categories,
        'stats': stats,
    })


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    category_slug = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search')

    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)
    if search:
        courses = courses.filter(title__icontains=search)

    categories = Category.objects.all()
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
        'selected_category': category_slug,
        'selected_level': level,
    })


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()
    reviews = course.reviews.select_related('student').all()[:10]
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        is_enrolled = enrollment is not None

    return render(request, 'courses/detail.html', {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    })


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user, course=course
    )
    if created:
        course.students_count += 1
        course.save()
        messages.success(request, f'"{course.title}" kursiga muvaffaqiyatli yozildingiz!')
    return redirect('lms:course', slug=slug)
