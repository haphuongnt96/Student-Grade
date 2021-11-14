from StudentGrades.repository import *

def calculate_average_mark(requestBody, midterm_weight):
    grade_average = requestBody["midterm_exam"] * midterm_weight + requestBody["final_term_exam"] * (1-midterm_weight)
    return grade_average