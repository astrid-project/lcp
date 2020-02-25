from colorama import Back, Fore, Style
from datetime import datetime
from requests.adapters import HTTPAdapter

import hashlib
import requests
import uuid


def exclude_keys_from_dict(dict_base, *keys):
    """
    Exclude the keys from the dictionary.

    :param dict_base: dictionary to check
    :keys: key to exclude from the dictionary
    :returns: dictionary without the keys
    """
    return {k: v for k, v in dict_base.items() if k not in keys}


def get_none(**vars):
    """
    Get the keys that are None value.

    :param vars: key/value arguments
    :returns: keys with value = None
    """
    res = []
    for text, var in vars.items():
        if var is None:
            res.append(text)
    return ', '.join(res)


def generate_username():
    """
    Generate a new password.

    :returns: new username
    """
    return str(uuid.uuid1())


def generate_password():
    """
    Generate a random password.

    :returns: random password
    """
    return hash(str(uuid.uuid1()))


def get_timestamp(ts = datetime.now()):
    """
    Set the timestamp in format %Y/%m/%d %H:%M:%S.

    :params ts: Timestamp to format
    :returns: Timestamp in format %Y/%m/%d %H:%M:%S
    """
    return ts.now().strftime('%Y/%m/%d %H:%M:%S')


def hash(text):
    """
    Make a hash of the text

    :param text: text to make the hash
    :returns: hashed version of the text
    """
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) in [list, tuple] else [data]
