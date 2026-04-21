from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('course/<slug:slug>/', views.course_player, name='course'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('quiz/<int:quiz_id>/', views.quiz_start, name='quiz_start'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
]
