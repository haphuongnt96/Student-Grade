from StudentGrades.models import Student, Course, Grade

def query_student(id=None):
    if not id:
        return Student.objects.all()
    return Student.objects.filter(id=id)

def query_insert_student(requestBody):
    new_student = Student(student_name=requestBody['student_name'], email=requestBody['email'], mobile_phone=requestBody['mobile_phone'])
    new_student.save()
    return new_student

def query_update_student(id, requestBody):
    update_student = Student(id=id, student_name=requestBody["student_name"], email=requestBody["email"], mobile_phone=requestBody["mobile_phone"])
    update_student.save()
    return update_student

def query_grade(student_id = None, course_id = None):
    if student_id and not course_id:
        return Grade.objects.filter(student=student_id).select_related('student', 'course')
    if course_id and not student_id:
        return Grade.objects.filter(course=course_id).select_related('student', 'course')

def query_insert_grade(requestBody, midterm_weight, grade_average, student_id = None, course_id = None):
    if student_id and not course_id:
        insert_grade = Grade(student=Student(id=student_id), course=Course(id=requestBody["course"]),midterm_exam_weight= midterm_weight, midterm_exam=requestBody["midterm_exam"], final_term_exam=requestBody["final_term_exam"], grade_average=grade_average)
        insert_grade.save()
        return insert_grade
    if course_id and not student_id:
        insert_grade = Grade(student=Student(id=requestBody["student"]), course=Course(id=course_id),midterm_exam_weight= midterm_weight, midterm_exam=requestBody["midterm_exam"], final_term_exam=requestBody["final_term_exam"], grade_average=grade_average)
        insert_grade.save()
        return insert_grade

def query_course(id=None):
    if not id:
        return Course.objects.all()
    return Course.objects.get(id=id)

def query_insert_course(requestBody):
    insert_course = Course(course_name=requestBody["course_name"], credit=requestBody["credit"], midterm_exam_weight=requestBody["midterm_exam_weight"])
    insert_course.save()
    return insert_course


def query_update_course(id, requestBody):
    update_course = Course(id=id, course_name=requestBody["course_name"], credit=requestBody["credit"], midterm_exam_weight=requestBody["midterm_exam_weight"])
    update_course.save()
    return update_course