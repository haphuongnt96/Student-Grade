from django.shortcuts import render
from StudentGrades.models import Grades
from django.db import models
import json
from django.core import serializers
# Create your views here.
from django.http import HttpResponse, HttpRequest


def greet(request: HttpRequest):
    name = request.GET.get('name', '')
    return render(request, "StudentGrades/index.html", {"name": name.capitalize()})

def info(request: HttpRequest, name):
    studentInfo = Grades.objects.get(name=name)
    data = serializers.serialize("json", [studentInfo])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    response = HttpResponse(data, content_type="application/json")
    #return render(request, "StudentGrades/index.html", {"name": studentInfo.grade1})
    return response


