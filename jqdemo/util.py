import datetime

def convert_date_to_datetime(dates):
    res = []
    for date in dates:
        res.append(datetime.datetime(date.year, date.month, date.day))
    return res
