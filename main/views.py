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
    return render(request, 'my_companies.html', context={'companies': Company.objects.filter(id__in=companies_ids), 'comp_user': companies_users[0]})


def change_role(request, id):
    userprofile = request.user.userprofile
    comp_user = userprofile.active_company_user
    if not comp_user:
        return HttpResponse('You hadn`t pick company')
    userprofile.active_company_user = CompanyUser.objects.get(role_id=id, company_id=comp_user.company_id, userprofile=userprofile)
    userprofile.save()
    return redirect(f'/main/enter_company/{comp_user.company_id}')


def enter_company(request, id):
    comp_user = request.user.userprofile.active_company_user
    if not comp_user or comp_user.company_id != id:
        comp_user = request.user.userprofile.companyuser_set.filter(company_id=id)[0]
    role_name = comp_user.role.name

    request.user.userprofile.active_company_user = comp_user
    request.user.userprofile.save()

    return {
        'admin': company_admin,
        'teacher': company_teacher,
        'student': company_student,
    }[role_name](request, comp_user.id)


def company_teacher(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    return HttpResponse('Сторінка поки не готова :(')

