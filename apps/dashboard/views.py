from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import JsonResponse
from apps.courses.models import Course, Module, Lesson, Enrollment, Category
from apps.accounts.models import User


@login_required
def home(request):
    user = request.user

    if user.role == 'admin' or user.is_staff:
        return admin_dashboard(request)
    elif user.role == 'mentor':
        return mentor_dashboard(request)
    elif user.role == 'curator':
        return curator_dashboard(request)
    else:
        return student_dashboard(request)


def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'dashboard/student.html', {
        'enrollments': enrollments,
        'total_courses': enrollments.count(),
        'completed': enrollments.filter(is_completed=True).count(),
        'in_progress': enrollments.filter(is_completed=False, progress__gt=0).count(),
    })


def mentor_dashboard(request):
    courses = Course.objects.filter(mentor=request.user)
    total_students = Enrollment.objects.filter(course__mentor=request.user).count()
    return render(request, 'dashboard/mentor.html', {
        'courses': courses,
        'total_students': total_students,
        'total_courses': courses.count(),
        'published': courses.filter(is_published=True).count(),
    })


def curator_dashboard(request):
    courses = Course.objects.filter(curator=request.user)
    mentor_courses = Course.objects.filter(mentor__isnull=False).select_related('mentor')
    students = User.objects.filter(role='student')
    return render(request, 'dashboard/curator.html', {
        'courses': courses,
        'mentor_courses': mentor_courses,
        'students': students,
        'total_students': students.count(),
        'total_courses': courses.count(),
    })


def admin_dashboard(request):
    stats = {
        'total_students': User.objects.filter(role='student').count(),
        'total_mentors': User.objects.filter(role='mentor').count(),
        'total_curators': User.objects.filter(role='curator').count(),
        'total_courses': Course.objects.count(),
        'published_courses': Course.objects.filter(is_published=True).count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    recent_users = User.objects.order_by('-date_joined')[:10]
    recent_courses = Course.objects.order_by('-created_at')[:5]
    return render(request, 'dashboard/admin.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
    })


# ============ CURATOR/MENTOR COURSE MANAGEMENT ============

@login_required
def create_course(request):
    if request.user.role not in ('mentor', 'curator', 'admin') and not request.user.is_staff:
        messages.error(request, 'Sizda bu sahifaga kirish huquqi yo\'q')
        return redirect('dashboard:home')

    if request.method == 'POST':
        title = request.POST.get('title')
        slug = title.lower().replace(' ', '-').replace("'", '')
        # Make slug unique
        base_slug = slug
        counter = 1
        while Course.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        course = Course(
            title=title,
            slug=slug,
            short_description=request.POST.get('short_description', ''),
            description=request.POST.get('description', ''),
            level=request.POST.get('level', 'beginner'),
            language=request.POST.get('language', 'uz'),
            duration_hours=int(request.POST.get('duration_hours', 0) or 0),
            is_free=request.POST.get('is_free') == 'on',
            price=float(request.POST.get('price', 0) or 0),
        )
        # Set category
        cat_id = request.POST.get('category')
        if cat_id:
            course.category_id = int(cat_id)

        if request.user.role == 'mentor':
            course.mentor = request.user
        elif request.user.role == 'curator':
            course.curator = request.user

        if request.FILES.get('thumbnail'):
            course.thumbnail = request.FILES['thumbnail']

        course.save()
        messages.success(request, f'"{course.title}" kursi yaratildi!')
        return redirect('dashboard:edit_course', pk=course.pk)

    categories = Category.objects.all()
    mentors = User.objects.filter(role='mentor')
    return render(request, 'dashboard/create_course.html', {
        'categories': categories,
        'mentors': mentors,
    })


@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role not in ('admin',) and not request.user.is_staff:
        if course.mentor != request.user and course.curator != request.user:
            messages.error(request, 'Ruxsat yo\'q')
            return redirect('dashboard:home')

    modules = course.modules.prefetch_related('lessons').all()
    categories = Category.objects.all()
    mentors = User.objects.filter(role='mentor')
    curators = User.objects.filter(role='curator')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_course':
            course.title = request.POST.get('title', course.title)
            course.short_description = request.POST.get('short_description', course.short_description)
            course.description = request.POST.get('description', course.description)
            course.level = request.POST.get('level', course.level)
            course.language = request.POST.get('language', course.language)
            course.duration_hours = int(request.POST.get('duration_hours', 0) or 0)
            course.is_free = request.POST.get('is_free') == 'on'
            course.price = float(request.POST.get('price', 0) or 0)
            course.is_published = request.POST.get('is_published') == 'on'
            cat_id = request.POST.get('category')
            if cat_id:
                course.category_id = int(cat_id)
            mentor_id = request.POST.get('mentor')
            if mentor_id:
                course.mentor_id = int(mentor_id)
            curator_id = request.POST.get('curator')
            if curator_id:
                course.curator_id = int(curator_id)
            if request.FILES.get('thumbnail'):
                course.thumbnail = request.FILES['thumbnail']
            course.save()
            messages.success(request, 'Kurs yangilandi!')

        elif action == 'add_module':
            Module.objects.create(
                course=course,
                title=request.POST.get('module_title'),
                order=course.modules.count() + 1
            )
            messages.success(request, 'Modul qo\'shildi!')

        elif action == 'add_lesson':
            module_id = request.POST.get('module_id')
            module = get_object_or_404(Module, id=module_id)
            lesson = Lesson(
                module=module,
                title=request.POST.get('lesson_title'),
                lesson_type=request.POST.get('lesson_type', 'video'),
                content=request.POST.get('content', ''),
                video_url=request.POST.get('video_url', ''),
                duration_minutes=int(request.POST.get('duration_minutes', 0) or 0),
                order=module.lessons.count() + 1,
                is_free_preview=request.POST.get('is_free_preview') == 'on',
            )
            if request.FILES.get('video_file'):
                lesson.video_file = request.FILES['video_file']
            lesson.save()
            messages.success(request, 'Dars qo\'shildi!')

        return redirect('dashboard:edit_course', pk=course.pk)

    return render(request, 'dashboard/edit_course.html', {
        'course': course,
        'modules': modules,
        'categories': categories,
        'mentors': mentors,
        'curators': curators,
    })


@login_required
def delete_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    course_pk = module.course.pk
    module.delete()
    messages.success(request, 'Modul o\'chirildi')
    return redirect('dashboard:edit_course', pk=course_pk)


@login_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_pk = lesson.module.course.pk
    lesson.delete()
    messages.success(request, 'Dars o\'chirildi')
    return redirect('dashboard:edit_course', pk=course_pk)


@login_required
def curator_students(request):
    if request.user.role not in ('curator', 'admin') and not request.user.is_staff:
        return redirect('dashboard:home')
    students = User.objects.filter(role='student').prefetch_related('enrollments')
    return render(request, 'dashboard/curator_students.html', {'students': students})


@login_required
def curator_mentors(request):
    if request.user.role not in ('curator', 'admin') and not request.user.is_staff:
        return redirect('dashboard:home')
    mentors = User.objects.filter(role='mentor').prefetch_related('teaching_courses')
    return render(request, 'dashboard/curator_mentors.html', {'mentors': mentors})
