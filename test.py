import calendar
import datetime


def get_dates(days_numbers, start_date: datetime.date, end_date: datetime.date):
    while start_date <= end_date:
        if start_date.weekday() + 1 in days_numbers:
            yield start_date
        start_date += datetime.timedelta(days=1)


print(list(get_dates([2, 3], datetime.date(year=2021, month=11, day=16), datetime.date.today())))
