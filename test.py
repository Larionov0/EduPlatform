# import calendar
# import datetime
#
#
# def get_dates(days_numbers, start_date: datetime.date, end_date: datetime.date):
#     while start_date <= end_date:
#         if start_date.weekday() + 1 in days_numbers:
#             yield start_date
#         start_date += datetime.timedelta(days=1)
#
#
# print(list(get_dates([2, 3], datetime.date(year=2021, month=11, day=16), datetime.date.today())))


def evklid_nsd(a, b):
    if b > a:
        a, b = b, a  # міняємо місцями

    x = a  # для вирішення нам потрібно пам'ятати тільки останні 2 елементи ряду, це й будуть x y
    y = b

    while True:
        new_el = x % y  # рахуємо залишок і-2 го на і-1 ше
        if new_el == 0:  # якщо залишок нульовий
            return y  # повертаємо попереднє число в ряді
        x, y = y, new_el  # заміняємо два  останні числа ряда (зміщуючи ряд вліво)


for pair in [(30, 20), (15, 5), (25, 15), (150, 60), (92, 7)]:
    print(f"Nsd of {pair} = {evklid_nsd(*pair)}")

