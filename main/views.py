from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required
from main.sub_views.admin import *
from main.sub_views.teacher import *
from main.sub_views.student import *
from .tools.functions import *


def subjects(request, id):
    comp_user = CompanyUser.objects.get(id=id)
    return render(request, 'subject_list.html', {'subjects': Subject.objects.filter(company=comp_user.company),
                                                 'comp_user': comp_user})


# Create your views here.
@login_required(login_url='/auth/sign_in')
def my_companies(request):
    companies_users = CompanyUser.objects.filter(userprofile=request.user.userprofile)
    companies_ids = set([company_user.company_id for company_user in companies_users])
    return render(request, 'my_companies.html', context={'companies': Company.objects.filter(id__in=companies_ids)})


def enter_company(request, id):
    comp_users = request.user.userprofile.companyuser_set.filter(company_id=id)
    comp_user = comp_users[0]
    role_name = comp_user.role.name
    return {
        'admin': company_admin,
        'teacher': company_teacher,
        'student': company_student,
    }[role_name](request, comp_user.id)


def company_teacher(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    return HttpResponse('Сторінка поки не готова :(')


def company_student(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    return HttpResponse('Сторінка поки не готова :(')


