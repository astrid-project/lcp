from datetime import datetime


def datetime_from_str(date_time_str, format='%Y/%m/%d %H:%M:%S'):
    """Get a datatime object from the string.

    :params date_time_str: datetime in string
    :params format: datetime format
    :returns datetime object
    """
    return datetime.strptime(date_time_str, format)


def datetime_to_str(date_time=None, format='%Y/%m/%d %H:%M:%S'):
    """Convert the datetime to string in the given format.

    :params data_time: datetime input
    :params format: datetime format
    :returns: datetime string in format %Y/%m/%d %H:%M:%S
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(format)
