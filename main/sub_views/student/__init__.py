from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from main.forms import *
import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required
from main.tools.functions import get_1day_date


def company_student(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    student = Student.objects.get(company_user_id=comp_user.id)
    groups = student.groups.all()
    for group in groups:
        group.stat = student.get_my_lessons_statistic_by_group(group)
        group.graph = go.Figure(data=[go.Pie(labels=['присутній', "відсутній"], values=[group.stat['present'], group.stat['total']-group.stat['present']])]).to_html()

    return render(request, 'student_groups.html', {'comp_user': comp_user, 'student': student, 'groups': groups})
