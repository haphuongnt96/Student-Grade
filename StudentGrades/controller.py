from django.db.models.fields import BigIntegerField
from StudentGrades.models import Student, Course, Grade
from StudentGrades.repository import *
from StudentGrades.services import *
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.core import serializers
import json
from django.db import models
from django.http import JsonResponse



#from StudentGrades.cache import 

###Caching###
class Node:
    def __init__(self, info):
        self.info = info
        self.next = None
        self.prev = None
        self.key = None


class LRUCache:
    def __init__(self):
        self.max_len = 3
        self.hash_table = {}
        self.tail = None
        self.head = None

    def get(self, key):
        if key in self.hash_table:
            # Move node to head
            if self.head.key != key:
                n = self.EvictNode(self.hash_table[key])
                self.insert(n, key)
                self.head = n
            return self.head.info
        return -1

    def insert(self, node, key):
        # Insert node to linked list head
        if not self.hash_table:
            self.head = self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node
        self.hash_table[key] = node
        self.head.key = key

    def EvictNode(self, node):
        # Unsert node from linked list
    
        if node == self.tail:
            # Delete from hash table
            del self.hash_table[self.tail.key]

            # Evict least recently used cache
            n = self.tail.prev
            self.tail.prev = None
            self.tail = n
            self.tail.next = None
        else:
            n1 = node.prev
            n2 = node.next
            n1.next = n2
            n2.prev = n1
        return node

cache = LRUCache()  #### Test Cache: get_one_student

# def hash_function()
def LRUDecorator(func):
    def wrapper(request, *args, **kwargs):
        # for kwarg, value in kwargs:
        #     print (kwarg,value)
        cache_info = cache.get(kwargs["id"])
        if cache_info == -1: #If data has not been cached
            if len(cache.hash_table) >= cache.max_len:
                cache.EvictNode(cache.tail)            
            data = func(request, kwargs["id"])
            n = Node(data)
            cache.insert(n, kwargs["id"])
            cache_info = cache.head.info
        
        print(cache_info)
        # print(f"cache.hash_table: {cache.hash_table}")
        # print(f"cache.head: {cache.head}")
        # print(f"cache.tail: {cache.tail}")
        # print(f"cache.head.key: {cache.head.key}")
        # print(f"cache.tail.key: {cache.tail.key}")
        # n1 = cache.head
        # while n1:
        #     print(n1.key)   
        #     n1 = n1.next
        return HttpResponse(cache_info, content_type="application/json")
    return wrapper


####Controller####
def transform_incoming_data(requestBody):
    data = requestBody.decode('utf-8')
    data_dict = json.loads(data)
    return data_dict

def get_all_students(request: HttpRequest):
    if request.method == 'GET':
        students = serializers.serialize('json', query_student())
        return HttpResponse(students, content_type="application/json")
    if request.method == 'POST':
        requestBody = transform_incoming_data(request.body)
        new_student = query_insert_student(requestBody)
        new_student = serializers.serialize('json', [new_student])
        return HttpResponse(new_student, content_type="application/json", status = 201)

# gen 200 Student
# 150

# 1->150

# 51 -> 150


# get 70 

# 51->150->70

# 30-> remove 51

# check cache 51


@LRUDecorator
def get_one_student(request: HttpRequest, student_id):
    if request.method == "GET":
        data = query_student(student_id)
            # Check if data presents in db
        if not data:
            return HttpResponseNotFound(f"Student id {student_id} not found")
        student = serializers.serialize('json', data)
        return student

    

    # if request.method == 'PUT':
    #     requestBody = transform_incoming_data(request.body)
    #     update_student = query_update_student(id, requestBody)
    #     update_student = serializers.serialize('json', [update_student])
    #     return HttpResponse(update_student, content_type="application/json", status = 201)

    # if request.method == 'DELETE':
    #     data.delete()
    #     return HttpResponse("Delete Successfully")

def grades_by_student(request: HttpRequest, id):
    data = query_student(id=id)
    if not data:
        return HttpResponseNotFound(f"Student id {id} not found")
    
    if request.method == "GET":   
        grade = query_grade(student_id=id)
        response = serializers.serialize('json', grade)
        return HttpResponse(response, content_type="application/json")

    if request.method == "POST":
        requestBody = transform_incoming_data(request.body)
        
        # Determine midterm weight
        course_info = query_course(id=requestBody["course"])
        midterm_weight = float(course_info.midterm_exam_weight)
        # Calculate average grade to save to database
        grade_average = calculate_average_mark(requestBody, midterm_weight)
        # Save to database
        new_grade = query_insert_grade(requestBody, midterm_weight, grade_average, student_id=id) 
        new_grade = serializers.serialize('json', [new_grade])
        return HttpResponse(new_grade, content_type="application/json", status = 201)


def get_all_courses(request: HttpRequest):
    if request.method == 'GET':
        courses = serializers.serialize('json', query_course())
        return HttpResponse(courses, content_type="application/json")
    if request.method == 'POST':
        requestBody = transform_incoming_data(request.body)
        new_course = query_insert_course(requestBody)
        new_course = serializers.serialize('json', [new_course])
        return HttpResponse(new_course, content_type="application/json", status = 201)

def get_one_course(request: HttpRequest, id):
    try:
        data = query_course(id=id)
    except:
        return HttpResponseNotFound(f"Course id {id} not found")
    else:
        if request.method == "GET":
            course = serializers.serialize('json', [data])
            return HttpResponse(course, content_type="application/json")

        if request.method == 'PUT':
            requestBody = transform_incoming_data(request.body)
            course_updated = query_update_course(id, requestBody)
            course_updated = serializers.serialize('json', [course_updated])
            return HttpResponse(course_updated, content_type="application/json", status = 201)

        if request.method == 'DELETE':
            data.delete()
            return HttpResponse("Delete Successfully")

def grades_by_course(request: HttpRequest, id):
    data = query_course(id=id)
    if not data:
        return HttpResponseNotFound(f"Course id {id} not found")
    
    if request.method == "GET":   
        grade = query_grade(course_id = id)
        response = serializers.serialize('json', grade)
        return HttpResponse(response, content_type="application/json")

    if request.method == "POST":
        requestBody = transform_incoming_data(request.body)
        # Determine midterm weight
        course_info = query_course(id=id)
        midterm_weight = float(course_info.midterm_exam_weight)
        # Calculate average grade to save to database
        grade_average = calculate_average_mark(requestBody, midterm_weight)
        # Save to database
        new_grade = query_insert_grade(requestBody, midterm_weight, grade_average, course_id=id) 
        new_grade = serializers.serialize('json', [new_grade])
        return HttpResponse(new_grade, content_type="application/json", status = 201)
