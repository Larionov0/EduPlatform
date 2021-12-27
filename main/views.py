from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *

from django.utils import timezone
from django.views.generic.list import ListView


def subjects(request, id):
    comp_user = CompanyUser.objects.get(id=id)
    return render(request, 'subject_list.html', {'subjects': Subject.objects.filter(company=comp_user.company),
                                                 'comp_user': comp_user})


# Create your views here.
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


def company_admin(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id, userprofile__user__id=request.user.id)
    company = comp_user.company

    return render(request, 'company_admin.html', {'company': company, 'comp_user': comp_user})


def company_teacher(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    return HttpResponse('Сторінка поки не готова :(')


def company_student(request, comp_user_id):
    comp_user = CompanyUser.objects.get(id=comp_user_id)
    return HttpResponse('Сторінка поки не готова :(')


def create_subject(request, id):
    comp_user = CompanyUser.objects.get(id=id)
    subject = Subject.objects.create(name='Новий предмет', company=comp_user.company)
    return redirect("main:edit_subject", comp_user.id, subject.id)


def edit_subject(request, id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    comp_user = CompanyUser.objects.get(id=id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save(comp_user.company_id)
            return redirect('main:subjects', id=id)
        else:
            print('invalid form')
    else:
        form = SubjectForm(instance=subject)

        return render(request, 'edit_subject.html', {'form': form, 'comp_user': comp_user, 'subject': subject})


def delete_subject(request, id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return redirect(f'/main/company/{id}/subjects')
