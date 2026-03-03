from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from apps.courses.models import Course, Lesson, Enrollment, LessonProgress, Module


@login_required
def course_player(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    modules = course.modules.prefetch_related('lessons').all()

    # Get first lesson or requested lesson
    lesson_id = request.GET.get('lesson')
    current_lesson = None
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    else:
        first_module = modules.first()
        if first_module:
            current_lesson = first_module.lessons.first()

    # Get completed lessons
    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        is_completed=True
    ).values_list('lesson_id', flat=True)

    # Calculate progress
    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_count = len(completed_lessons)
    progress = int((completed_count / total_lessons * 100) if total_lessons > 0 else 0)

    # Update enrollment progress
    enrollment.progress = progress
    enrollment.save()

    return render(request, 'lms/player.html', {
        'course': course,
        'modules': modules,
        'current_lesson': current_lesson,
        'completed_lessons': list(completed_lessons),
        'progress': progress,
        'enrollment': enrollment,
    })


@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=lesson.module.course)

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user, lesson=lesson
    )
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

    # Recalculate
    total = Lesson.objects.filter(module__course=lesson.module.course).count()
    done = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=lesson.module.course,
        is_completed=True
    ).count()
    pct = int(done / total * 100) if total else 0
    enrollment.progress = pct
    if pct == 100:
        enrollment.is_completed = True
    enrollment.save()

    return JsonResponse({'success': True, 'progress': pct})
