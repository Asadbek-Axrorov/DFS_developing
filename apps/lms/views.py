from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from apps.courses.models import Course, Lesson, Enrollment, LessonProgress, Quiz, QuizAttempt, QuizAnswer, Choice


@login_required
def course_player(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    modules = course.modules.prefetch_related('lessons').all()

    lesson_id = request.GET.get('lesson')
    current_lesson = None
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    else:
        first_module = modules.first()
        if first_module:
            current_lesson = first_module.lessons.first()

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        is_completed=True
    ).values_list('lesson_id', flat=True)

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_count = len(completed_lessons)
    progress = int((completed_count / total_lessons * 100) if total_lessons > 0 else 0)

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


@login_required
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    lesson = quiz.lesson
    course = lesson.module.course

    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    attempts_count = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
    if quiz.max_attempts > 0 and attempts_count >= quiz.max_attempts:
        messages.error(request, f"Siz {quiz.max_attempts} ta urinishdan foydalandingiz!")
        return redirect('lms:course', slug=course.slug)

    prev_attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz).order_by('-started_at')
    questions = quiz.questions.prefetch_related('choices').all()

    if request.method == 'POST':
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            total_points=quiz.total_points(),
            finished_at=timezone.now()
        )

        score = 0
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    selected = Choice.objects.get(id=choice_id, question=question)
                    is_correct = selected.is_correct
                    if is_correct:
                        score += question.points
                    QuizAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=selected,
                        is_correct=is_correct
                    )
                except Choice.DoesNotExist:
                    pass

        attempt.score = score
        total = quiz.total_points()
        attempt.percentage = round((score / total * 100), 1) if total > 0 else 0
        attempt.is_passed = attempt.percentage >= quiz.pass_percentage
        attempt.save()

        return redirect('lms:quiz_result', attempt_id=attempt.id)

    return render(request, 'lms/quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'lesson': lesson,
        'course': course,
        'attempts_count': attempts_count,
        'prev_attempts': prev_attempts,
    })


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    answers = attempt.answers.select_related(
        'question', 'selected_choice'
    ).prefetch_related('question__choices').all()
    course = attempt.quiz.lesson.module.course

    return render(request, 'lms/quiz_result.html', {
        'attempt': attempt,
        'answers': answers,
        'course': course,
        'quiz': attempt.quiz,
    })
