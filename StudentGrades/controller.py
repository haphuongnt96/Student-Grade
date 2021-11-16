from django.db.models.fields import BigIntegerField
from StudentGrades.models import Student, Course, Grade
from StudentGrades.repository import *
from StudentGrades.services import *
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.core import serializers
import json
from django.db import models
from django.http import JsonResponse

class student_form:
    def __init__(self, student_name: str, email: str, mobile_phone: str):
        #Run validations to the received arguments
        if not isinstance(student_name, str):
            raise TypeError("Student name must be of type str")
        elif not isinstance(email, str):
            raise TypeError("Email must be of type str")
        elif not isinstance(mobile_phone, str)
            raise TypeError("Mobile phone must be of type str")

        # Assign to self object
        self.student_name = str(student_name)
        self.email = str(email)
        self.mobile_phone = str(mobile_phone)

class course_form:
    def __init__(self, course_name: str, credit: int, midterm_exam_weight: float):
        #Validate data types
        if not isinstance(course_name, str):
            raise TypeError("Course name must be of type str")
        elif not isinstance(credit, int):
            raise TypeError("Credit must be of type int")
        elif not isinstance(midterm_exam_weight, float)
            raise TypeError("midterm_exam_weight must be of type float")

        #Run validations to the received arguments
        if midterm_exam_weight > 1 or midterm_exam_weight < 0:
            raise Exception("Midterm weight must be between 0 and 1")
        if credit < 0:
            raise Exception("credit must be > 0")

        # Assign to self object
        self.course_name = str(course_name)
        self.credit = int(credit)
        self.midterm_exam_weight = float(midterm_exam_weight)

class grade_form:
    def __init__(self, student: int, course: int, midterm_exam_weight: float, midterm_exam: float, final_term_exam: float, grade_average: float):
        if not isinstance(student, int):
            raise TypeError("Student id must be of type int")
        elif not isinstance(course, int):
            raise TypeError("Course id must be of type int")
        elif not isinstance(midterm_exam_weight, float)
            raise TypeError("midterm_exam_weight must be of type float")
        elif not isinstance(midterm_exam, float)
            raise TypeError("midterm_exam must be of type float")
        elif not isinstance(final_term_exam, float)
            raise TypeError("final_term_exam must be of type float")
        elif not isinstance(grade_average, float)
            raise TypeError("grade_average must be of type float")

        self.student_id = int(student)
        self.course_id = int(course)
        self.midterm_exam_weight = float(midterm_exam_weight)
        self.midterm_exam = float(midterm_exam)
        self.final_term_exam = float(final_term_exam)
        self.grade_average = float(grade_average)

def transform_incoming_data():
    data = request.body.decode('utf-8')
    data_dict = json.loads(data)
    return data_dict

def get_all_students(request: HttpRequest):
    if request.method == 'GET':
        students = serializers.serialize('json', query_student())
        return HttpResponse(students, content_type="application/json")
    if request.method == 'POST':
        requestBody = transform_incoming_data())
        requestBody = student_form(requestBody['student_name'], requestBody['email'], requestBody['mobile_phone'])
        new_student = query_insert_student(requestBody)
        new_student = serializers.serialize('json', [new_student])
        return HttpResponse(new_student, content_type="application/json", status = 201)

def get_one_student(request: HttpRequest, id):
    data = query_student(id=id)
    if not data:
        return HttpResponseNotFound(f"Student id {id} not found")

    if request.method == "GET":
        student = serializers.serialize('json', data)
        return HttpResponse(student, content_type="application/json")

    if request.method == 'PUT':
        requestBody = transform_incoming_data(request.body)
        update_student = query_update_student(id, requestBody)
        update_student = serializers.serialize('json', [update_student])
        return HttpResponse(update_student, content_type="application/json", status = 201)

    if request.method == 'DELETE':
        data.delete()
        return HttpResponse("Delete Successfully")

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
        #requestBody = transform_incoming_data(request.body)
        requestBody = transform_incoming_data(request.body)

        requestBody = course_v(requestBody['course_name'], requestBody['credit'], requestBody['midterm_exam_weight'])
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
        