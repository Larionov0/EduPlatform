from django.db import models
from authsys.models import UserProfile
import datetime
import calendar
import random


# Create your models here.
class Company(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, blank=True)

    C_t_min = models.IntegerField(default=0)  # %
    C_s_min = models.IntegerField(default=0)

    p_t_ser = models.FloatField(default=6)
    p_s_ser = models.FloatField(default=5)

    @property
    def students_amount(self):  # FIXME: wrong way
        # return Student.objects.count()
        return CompanyUser.objects.filter(company=self, role__name='student').count()

    def calculate_income(self):
        return sum(group.calculate_students_payment() for group in Group.objects.filter(course__subject__company=self))

    def calculate_spends(self):
        return sum(group.calculate_teacher_payment() for group in Group.objects.filter(course__subject__company=self))

    def calculate_income_last_month(self):
        return sum(group.calculate_students_payment(datetime.date.today()) for group in Group.objects.filter(course__subject__company=self))

    def calculate_spends_last_month(self):
        return sum(group.calculate_teacher_payment(datetime.date.today()) for group in Group.objects.filter(course__subject__company=self))

    def calculate_income_for_month(self, month: datetime.date):
        return sum(group.calculate_students_payment(month) for group in Group.objects.filter(course__subject__company=self))

    def calculate_spends_for_month(self, month: datetime.date):
        return sum(group.calculate_teacher_payment(month) for group in Group.objects.filter(course__subject__company=self))

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
    complexity = models.IntegerField(default=80)

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def calculate_students_payment(self, month: datetime.date=None):
        if month:
            lessons = Lesson.objects.filter(
                date_start__gte=datetime.date(month.year, month.month, 1),
                date_start__lte=datetime.date(month.year, month.month, calendar.monthrange(month.year, month.month)[1]),
                group=self
            )
        else:
            lessons = Lesson.objects.filter(group=self)
        return sum([lesson.calc_student_payment() * lesson.present_students.count() for lesson in lessons])

    def calculate_teacher_payment(self, month: datetime.date=None):
        if month:
            lessons = Lesson.objects.filter(
                date_start__gte=datetime.date(month.year, month.month, 1),
                date_start__lte=datetime.date(month.year, month.month, calendar.monthrange(month.year, month.month)[1]),
                group=self
            )
        else:
            lessons = Lesson.objects.filter(group=self)
        return sum([lesson.calc_teacher_payment() for lesson in lessons])

    def when_is_next_lesson(self):
        planned_lessons = list(self.plannedlesson_set.all())
        dt = datetime.datetime.now()
        today_planned = [pl for pl in planned_lessons if pl.day==dt.weekday()+1 and pl.time_start >= dt.time()]
        if today_planned:
            return today_planned[0]

        dat = dt.date()
        for i in range(10):
            dat = dat + datetime.timedelta(days=1)
            planned = [pl for pl in planned_lessons if pl.day == dat.weekday() + 1]
            if planned:
                return planned[0]

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
    presence_chance = models.IntegerField(default=100)  # 0 to 100

    def get_my_lessons_statistic_by_group(self, group):
        # FIXME: add date of start being in group checking
        lessons = group.lesson_set.all()
        be = 0
        total = 0
        for lesson in lessons:
            if lesson.present_students.filter(id=self.id).exists():
                be += 1
            total += 1

        return {'present': be, 'total': total}


class Teacher(RoleUser):
    groups = models.ManyToManyField(Group, related_name='teachers')  # учителей может быть больше одного
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')  # курсы которые ведет в этой компании
    rang = models.IntegerField(default=1)
    professionalism = models.IntegerField(default=50)

    def calc_salary_for_cur_month(self, company=None):
        if company is None:
            return sum([group.calculate_teacher_payment(datetime.date.today()) for group in self.groups.all()])
        else:
            return sum([group.calculate_teacher_payment(datetime.date.today()) for group in self.groups.filter(course__subject__company=company)])


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


def get_dates(days_numbers, start_date: datetime.date, end_date: datetime.date):
    while start_date <= end_date:
        if start_date.weekday() + 1 in days_numbers:
            yield start_date
        start_date += datetime.timedelta(days=1)


class Lesson(models.Model):
    time_start = models.TimeField()
    date_start = models.DateField()
    name = models.CharField(max_length=60)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    planned_lesson = models.ForeignKey(PlannedLesson, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    duration = models.IntegerField(default=90)
    present_students = models.ManyToManyField(Student, related_name='lessons')

    @classmethod
    def create_from_planed(cls, planned_lesson: PlannedLesson, date: datetime.date):
        return cls.objects.get_or_create(
            time_start=planned_lesson.time_start,
            date_start=date,
            planned_lesson=planned_lesson,
            group=planned_lesson.group,
            duration=planned_lesson.duration,
            defaults=dict(
                name='',
            )
        )[0]

    @classmethod
    def autogenerate_for_period(cls, group: Group, delta_from_now=datetime.timedelta(days=60)):
        planned_lessons = group.plannedlesson_set.all()
        today = datetime.date.today()
        planned_dict = {}
        for lesson in planned_lessons:
            planned_dict[lesson.day] = lesson
        dates = get_dates(list(planned_dict.keys()), today-delta_from_now, today)
        for date in dates:
            planned = planned_dict[date.weekday() + 1]
            lesson = cls.create_from_planed(planned, date)
            for student in group.students.all():
                if random.randint(1, 100) > student.presence_chance:
                    lesson.present_students.add(student)

    def calc_student_payment(self):
        if self.group.students.count() == 0:
            return 0
        return self.group.course.student_payment * (1 / (self.group.students.count() ** 0.5))

    def calc_teacher_payment(self):
        return self.group.course.teacher_payment * (self.present_students.count() ** 0.5)

    def __str__(self):
        return f"{self.name} ({self.date_start}  {self.time_start})  ({self.duration} m)"
