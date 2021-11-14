from django.shortcuts import render
#from StudentGrades.models import Grades
from django.db import models
import json
from django.core import serializers
# Create your views here.
from django.http import HttpResponse, HttpRequest





def greet(request: HttpRequest):
    return HttpResponse("Phedra's Project")


