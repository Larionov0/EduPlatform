# сдвинуть уроки
from main.models import Lesson
from datetime import timedelta


def offset_lessons(days_offset=140):
    for lesson in Lesson.objects.all():
        print(f"Done with lesson {lesson.id}")
        lesson.date_start = lesson.date_start + timedelta(days=days_offset)
        lesson.save()


def run():
    offset_lessons()

#
# if __name__ == '__main__':
#     run()
