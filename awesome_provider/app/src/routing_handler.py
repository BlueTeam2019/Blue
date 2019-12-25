from datetime import datetime


def validate_time_format(time_to_validate):
    date_format = '%Y%m%d%H%M%S'
    try:
        date_obj = datetime.strptime(time_to_validate, date_format)
        return True
    except ValueError as e:
        raise ValueError(f"Incorrect data format, {date_format} " \
              f"should be YYYYMMDDHHMMSS \b {e}")
