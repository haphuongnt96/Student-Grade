from django.urls import path

from . import views
from . import controller

urlpatterns = [
    path('', views.greet, name='greet'),
    path('students/', controller.get_all_students, name='all students'),
    path('students/<int:id>/', controller.get_one_student, name='a student'),
    path('students/<int:id>/grades', controller.grades_by_student, name='grades by student'),
    path('courses/', controller.get_all_courses, name='all courses'),
    path('courses/<int:id>/', controller.get_one_course, name='a course'),
    path('courses/<int:id>/grades', controller.grades_by_course, name='grades by course'),
]