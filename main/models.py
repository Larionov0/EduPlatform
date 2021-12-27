from django.db import models
from authsys.models import UserProfile


# Create your models here.
class Company(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.name}'


class Role(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"


class CompanyUser(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    date_join = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.userprofile} - {self.company} - {self.role}"


class Subject(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.course})"


class RoleUserMixin:
    company_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)

    @property
    def userprofile(self):
        return self.company_user.userprofile

    def __str__(self):
        return f"{self.userprofile.user.username}"


class Student(models.Model, RoleUserMixin):
    groups = models.ManyToManyField(Group, blank=True, related_name='students')
    average_mark = models.IntegerField(default=0)  # необязательное поле для относительной оценки обучаемости студентов преподом


class Teacher(models.Model, RoleUserMixin):
    groups = models.ManyToManyField(Group, related_name='teachers')  # учителей может быть больше одного
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')  # курсы которые ведет в этой компании
    rang = models.IntegerField(default=1)


class Admin(models.Model, RoleUserMixin):
    is_superadmin = models.BooleanField(default=False)
