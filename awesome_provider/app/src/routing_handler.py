from datetime import datetime


def validate_time_format(time_to_validate):
    date_format = '%Y%m%d%H%M%S'
    try:
        date_obj = datetime.strptime(time_to_validate, date_format)
        print(date_obj)
        return True
    except ValueError:
        return False, "Incorrect data format, should be YYYYMMDDHHMMSS"
