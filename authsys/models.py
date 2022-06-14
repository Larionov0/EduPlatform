from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    info = models.TextField(max_length=1000, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    active_company_user = models.OneToOneField('main.CompanyUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='u_dont_need_it')

    @classmethod
    def create_from_user(cls, user):
        return cls.objects.create(user=user)
    
    @property
    def my_companies(self):
        # lst = list(set([company_user.company for company_user in self.companyuser_set.all()]))
        companies = []
        ids = []
        for c_user in self.companyuser_set.all():
            company = c_user.company
            if company.id in ids:
                continue
            company.selected = c_user.id == self.active_company_user_id
            ids.append(company.id)
            companies.append(company)

        # print([comp.selected for comp in lst])
        return companies

    @property
    def available_roles(self):
        if not self.active_company_user:
            return []

        roles = []
        for company_user in self.companyuser_set.filter(company=self.active_company_user.company):
            role = company_user.role
            role.selected = self.active_company_user_id == company_user.id
            roles.append(role)

        return roles

    def __str__(self):
        return f"Profile {self.user}"
