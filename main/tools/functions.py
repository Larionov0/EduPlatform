import datetime


def get_1day_date(date):
    return datetime.date(year=date.year, month=date.month, day=1)
