import requests
from requests.adapters import HTTPAdapter


def exclude_keys_from_dict(dict_base, *keys):
    return {k: v for k, v in dict_base.items() if k not in keys}


def get_none(**vars):
    res = []
    for text, var in vars.items():
        if var is None:
            res.append(text)
    return ', '.join(res)


def wrap(data):
    return data if type(data) in [list, tuple] else [data]
