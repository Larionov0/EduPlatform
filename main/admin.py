from django.contrib import admin
from .models import *

# Register your models here.
for model in (Company, Role, CompanyUser, Subject, Course, Group, Student, Teacher, Admin, PlannedLesson, Lesson):
    admin.site.register(model)
