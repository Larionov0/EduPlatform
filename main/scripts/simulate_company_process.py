import datetime
from main.models import *


def simulate(comp_name, start_date, end_date):
    company = Company.objects.get(name=comp_name)

    while start_date <= end_date:
        planned_lessons = PlannedLesson.objects.filter(day=start_date.weekday())
        for planned in planned_lessons:
            Lesson.create_from_planed(planned, start_date)

        start_date = start_date + datetime.timedelta(days=1)


def run():
    pass
