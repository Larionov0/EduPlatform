import datetime
from main.models import *


def simulate(comp_name, days=30):
    company = Company.objects.get(name=comp_name)
    for subject in company.subject_set.all():
        for course in subject.course_set.all():
            for group in course.group_set.all():
                print(f"Generating studying process for {group}...")
                Lesson.autogenerate_for_period(group, datetime.timedelta(days=days))

    # while start_date <= end_date:
    #     planned_lessons = PlannedLesson.objects.filter(day=start_date.weekday()+1)
    #     for planned in planned_lessons:
    #         Lesson.create_from_planed(planned, start_date)
    #
    #     start_date = start_date + datetime.timedelta(days=1)


def run():
    simulate('simulated1')
