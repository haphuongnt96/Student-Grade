import pytest

from django.core.management import call_command
from StudentGrades.models import *

# @pytest.fixture(scope='module', autouse=True)
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         pass
#         # for i in range(200):
#         #     student = Student.objects.create(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789")

#         #     student = Student.objects.get(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789")

# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass