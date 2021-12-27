from django.db import models
from authsys.models import UserProfile
import datetime


# Create your models here.
class Company(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, blank=True)

    def calculate_income(self):
        return 0

    def calculate_spends(self):
        return 0

    def calculate_income_last_month(self):
        return 0

    def calculate_spends_last_month(self):
        return 0

    @property
    def courses(self):
        subjects = Subject.objects.filter(company=self)
        return Course.objects.filter(subject__in=subjects)

    @property
    def courses_amount(self):
        return len(self.courses)

    @property
    def groups(self):
        return Group.objects.filter(course__in=self.courses)

    @property
    def groups_amount(self):
        return len(self.groups)

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
    description = models.TextField(max_length=1000, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.company})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    teacher_payment = models.IntegerField(default=200)
    student_payment = models.IntegerField(default=350)

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.course})"


class RoleUser(models.Model):
    company_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)

    @property
    def userprofile(self):
        return self.company_user.userprofile

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.userprofile.user.username}"


class Student(RoleUser):
    groups = models.ManyToManyField(Group, blank=True, related_name='students')
    average_mark = models.IntegerField(default=0)  # необязательное поле для относительной оценки обучаемости студентов преподом


class Teacher(RoleUser):
    groups = models.ManyToManyField(Group, related_name='teachers')  # учителей может быть больше одного
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')  # курсы которые ведет в этой компании
    rang = models.IntegerField(default=1)


class Admin(RoleUser):
    is_superadmin = models.BooleanField(default=False)


class PlannedLesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    time_start = models.TimeField()
    duration = models.IntegerField(default=90)  # у хвилинах
    day = models.IntegerField(default=1)

    days = {
        1: 'понеділок',
        2: 'вівторок',
        3: 'середа',
        4: 'четвер',
        5: 'п`ятниця',
        6: 'субота',
        7: 'неділя',
    }

    def __str__(self):
        return f"{self.days[self.day]} {self.time_start}  ({self.duration} m) - {self.group}"


class Lesson(models.Model):
    time_start = models.TimeField()
    date_start = models.TimeField()
    name = models.CharField(max_length=60)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    planned_lesson = models.ForeignKey(PlannedLesson, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    duration = models.IntegerField(default=90)
    present_students = models.ManyToManyField(Student, related_name='lessons')

    @classmethod
    def create_from_planed(cls, planned_lesson: PlannedLesson, date: datetime.date):
        return cls.create(
            time_start=planned_lesson.time_start,
            date_start=date,
            name='',
            group=planned_lesson.group,
            planned_lesson=planned_lesson,
            duration=planned_lesson.duration,
        )

    @classmethod
    def autogenerate_for_period(cls, months=2):
        pass


    def __str__(self):
        return f"{self.name} ({self.date_start}  {self.time_start})  ({self.duration} m)"
