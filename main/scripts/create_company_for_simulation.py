from main.models import *
from authsys.models import *
import random


stud_names = ['Bob', 'Illya', 'Alina', 'Anna', 'Inna', 'Tom', 'Richard', 'John', 'Jack', 'Alex', 'Alan', 'Relko', 'Ivan', 'George', 'Inokentiy']
stud_surnames = ['Bobenko', 'Illenko', 'Kachinski', 'Bobinski', 'Plushchenko', 'Koropadko', 'Dido', 'Johnsonuk', 'Cooc', 'Williams']


disc_names = ['Математика', "Укр література", "Укр мова", "Програмування", "Бази даних"]


def generate_company(students_amount, name, C_t_min, C_s_min, p_t_ser, p_s_ser, disciplines_amount, courses_amount, groups_amount):
    company = Company.objects.create(
        owner=UserProfile.objects.get(user=User.objects.get(username='admin')),
        name=name,
        description='',
        C_t_min=C_t_min,
        C_s_min=C_s_min,
        p_t_ser=p_t_ser,
        p_s_ser=p_s_ser
    )

    subjects = []
    for i in range(disciplines_amount):
        subjects.append(Subject.objects.create(name=random.choice(disc_names), company=company))

    courses = []
    for i in range(courses_amount):
        subject = random.choice(subjects)
        courses.append(Course.objects.create(
            name=f'{subject.name}-{random.randint(100, 999)}',
            description='Автоматично згенерований курс',
            subject=subject,
            complexity=random.randint(40, 90)
        ))

    groups = []
    for i in range(groups_amount):
        course = random.choice(courses)
        group = Group.objects.create(
            name=f"{random.choice(['A','B','C','D','E','F','G','H','I','J'])}-{random.randint(0, 999)}",
            description='Автоматично згенерована група',
            course=course
        )
        groups.append(group)

        PlannedLesson.objects.create(
            group=group,
            time_start=datetime.time(hour=16, minute=30),
            duration=60,
            day=1
        )
        if random.randint(0, 1):
            PlannedLesson.objects.create(
                group=group,
                time_start=datetime.time(hour=18, minute=0),
                duration=60,
                day=5
            )

    print('all done, now students:')
    all_students = []
    for i in range(students_amount):
        if i % 10 == 0:
            print(f'Done with {i} students')
        name = random.choice(stud_names)
        surname = random.choice(stud_surnames)

        user = User.objects.create_user(username=f"{name} {surname} {random.randint(100,999)}", password=surname)
        userprofile = UserProfile.objects.create(user=user, name=name, surname=surname)
        company_user = CompanyUser.objects.create(
            company=company,
            userprofile=userprofile,
            role=Role.objects.get(name='student'),
        )
        student = Student.objects.create(presence_chance=random.randint(60, 100), company_user=company_user)
        all_students.append(student)


def run():
    generate_company(50, 'simulated3', -10, 4, 6.25, 5, 3, 5, 10)
