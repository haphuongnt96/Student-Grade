from StudentGrades.controller import *
from django.test import RequestFactory
import pytest


factory = RequestFactory()

@pytest.mark.django_db
def setup_module(module):
    pass
    #for i in range(200):
    #    student = Student.objects.create(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789")

@pytest.mark.django_db
def test_get_one_student():
    # Get student 150
    request = factory.get('/students/150')
    print(get_one_student(request, id=150))
    # Check 
    # assert cache.head is not None
    # assert cache.head = cache.detail
    pass

@pytest.mark.django_db
def teardown_module(module):
    # for i in range(200):
    #     student = Student.objects.get(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789")
    #     student.delete()
    # student = Student.objects.filter()
    pass
    