from django.core.management import call_command
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduPlatform.settings")
django.setup()
from main.models import *
from authsys.models import *
import pathlib


def main():
    call_command('migrate')

    users = [
        {
            'name': 'Анна',
            'surname': "Василенко",
        },
        {
            'name': 'Роман',
            'surname': "Васько",
        },
        {
            'name': 'Ілля',
            'surname': "Меленюк",
        },
        {
            'name': 'Катерина',
            'surname': "Ігнатенко",
        },
        {
            'name': 'Олена',
            'surname': "Трущенко",
        },
        {
            'name': 'Федір',
            'surname': "Біляков",
        },
        {
            'name': 'Ігор',
            'surname': "Рудий",
        },
        {
            'name': 'Олександр',
            'surname': "Олешко",
        }
    ]

    for user_dict in users:
        user = User.objects.create_user(username=user_dict['surname'], password=user_dict['surname'])
        userprofile = UserProfile.objects.create(user=user, name=user_dict['name'], surname=user_dict['surname'])
    print('Users created')


if __name__ == '__main__':
    main()
