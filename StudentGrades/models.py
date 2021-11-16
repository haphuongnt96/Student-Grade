from django.db import models

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_phone = models.CharField(max_length=12)

    def __str__(self):
        return f"[student_id={self.id}, student_name={self.student_name}, email={self.email}, mobile_phone={self.mobile_phone}]"

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    credit = models.IntegerField()
    midterm_exam_weight = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"course_id={self.id}, course_name={self.course_name}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    midterm_exam_weight = models.DecimalField(max_digits=2, decimal_places=1)
    midterm_exam = models.DecimalField(max_digits=3, decimal_places=1)
    final_term_exam = models.DecimalField(max_digits=3, decimal_places=1)
    grade_average = models.DecimalField(max_digits=3, decimal_places=1)
    
    def __str__(self):
        return f"grade_id={self.id}, student_id={self.student}, course_id={self.course}, grade={self.grade_average}"



