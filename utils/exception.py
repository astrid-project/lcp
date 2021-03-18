import os
import sys
from pathlib import Path

__all__ = [
    'extract_info',
    'to_str'
]


def extract_info(exception):
    try:
        reason = eval(str(exception))
    except Exception:
        reason = str(exception)
    output = dict(reason=reason)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if exc_tb:
        filename = exc_tb.tb_frame.f_code.co_filename
        output.update(filename=filename, line=exc_tb.tb_lineno)
    return output


def to_str(exception):
    info = extract_info(exception)
    if 'filename' in info and 'line' in info:
        return f'{info["reason"]} on filename:{info["filename"]} at line:{info["line"]}'
    else:
        return info["reason"]
