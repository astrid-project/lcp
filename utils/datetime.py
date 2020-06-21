from datetime import datetime

__all__ = [
    'FORMAT',
    'datetime_from_str',
    'datetime_to_str'
]

FORMAT = '%Y/%m/%d %H:%M:%S'


def datetime_from_str(date_time_str, format=FORMAT):
    """Get a datatime object from the string.

    :params date_time_str: datetime in string
    :params format: datetime format
    :returns datetime object
    """
    return datetime.strptime(date_time_str, format)


def datetime_to_str(date_time=None, format=FORMAT):
    """Convert the datetime to string in the given format.

    :params data_time: datetime input
    :params format: datetime format
    :returns: datetime string in the given format
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(format)
