from StudentGrades.controller import *
from django.test import RequestFactory
from unittest.mock import patch
import pytest


factory = RequestFactory()
students = {}

def mocked_student(id):
    return students[id]

# @pytest.mark.django_db
def setup_module(module):   
    for i in range(200):
        #students[i] ={"student_name": f"Student{i}", "email": f"student{i}@example.com", "mobile_phone":"0123456789 "}
        students[i] = [Student(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789 ")]

#@pytest.mark.django_db
@patch("StudentGrades.controller.query_student", mocked_student)
def test_get_one_student():
    # cache mac_len = 3
    # Get student 150
    request = factory.get('/students/150') 
    print(get_one_student(request, id=150))

    ## Cache (hash table)
    ## Linked list
    assert len(cache.hash_table) == 1
    assert cache.head.key == cache.tail.key == 150
    assert cache.hash_table[150] == cache.head == cache.tail

    print(get_one_student(request, id=51))
    assert len(cache.hash_table) == 2
    assert cache.head.key == 51 
    assert cache.tail.key == 150
    assert cache.hash_table[150] == cache.tail
    assert cache.hash_table[51] == cache.head

    print(get_one_student(request, id=70))
    assert len(cache.hash_table) == 3
    assert cache.head.key == 70
    assert cache.head.next.key == 51 
    assert cache.head.next.next.key == cache.tail.key == 150
    assert cache.hash_table[150] == cache.tail
    assert cache.hash_table[70] == cache.head

    print(get_one_student(request, id=30))
    assert len(cache.hash_table) == 3
    assert cache.head.key == 30
    assert cache.head.next.key == 70 
    assert cache.head.next.next.key == cache.tail.key == 51
    assert cache.hash_table[51] == cache.tail
    assert cache.hash_table[30] == cache.head
    
    assert 150 not in cache.hash_table

    print(get_one_student(request, id=70))
    assert len(cache.hash_table) == 3
    assert cache.head.key == 70
    assert cache.head.next.key == 30 
    assert cache.head.next.next.key == cache.tail.key == 51
    assert cache.hash_table[51] == cache.tail
    assert cache.hash_table[70] == cache.head

# @pytest.mark.django_db
def teardown_module(module):
    # for i in range(200):
    #     student = Student.objects.get(student_name=f"Student{i}", email=f"student{i}@example.com", mobile_phone="0123456789")
    #     student.delete()
    # student = Student.objects.filter()
    pass