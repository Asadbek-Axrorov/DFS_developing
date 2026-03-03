from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('create-course/', views.create_course, name='create_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete-module/<int:pk>/', views.delete_module, name='delete_module'),
    path('delete-lesson/<int:pk>/', views.delete_lesson, name='delete_lesson'),
    path('curator/students/', views.curator_students, name='curator_students'),
    path('curator/mentors/', views.curator_mentors, name='curator_mentors'),
]
