from pathlib import Path

import os
import sys

__all__ = [
    'extract_info',
    'to_str'
]


def extract_info(exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    try:
        reason = eval(str(exception))
    except Exception:
        reason = str(exception)
    return dict(reason=reason, filename=filename, line=exc_tb.tb_lineno)


def to_str(exception):
    info = extract_info(exception)
    return f'{info["reason"]} on filename:{info["filename"]} at line:{info["line"]}'
