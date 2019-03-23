import datetime


def convert_date_to_datetime(dates):
    list = []
    for date in dates:
        list.append(datetime.datetime(date.year, date.month, date.day))
    return list