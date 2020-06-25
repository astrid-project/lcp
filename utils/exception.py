from pathlib import Path

import os
import sys

__all__ = [
    'extract_info',
    'reload_import',
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


def reload_import(error):
    error_data = str(error).split()
    if ['cannot', 'import'] == error_data[0:2]:
        name = error_data[2]
        path = Path(__file__).parent / '../requirements.txt'
        with path.open('r') as req_file:
            for mod in req_file:
                if mod == name.replace('_', '-'):
                    os.system('pip3 install -r requirements.txt')
                    break
    print(f'Error: {error}')
    sys.exit(1)


def to_str(exception):
    info = extract_info(exception)
    return f'{info["reason"]} on filename:{info["filename"]} at line:{info["line"]}'
