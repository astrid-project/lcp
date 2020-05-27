def exclude_keys(dict_base, *keys):
    """
    Exclude the keys from the dictionary.

    :param dict_base: dictionary to check
    :keys: key to exclude from the dictionary
    :returns: dictionary without the keys
    """
    return {k: v for k, v in dict_base.items() if k not in keys}


def iterate(source, *keys):
    """
    Iterate a nested dict based on list of keys

    :param source: nested dict
    :param *keys: list of keys
    :returns: value
    """
    d = source
    for k in keys:
        if type(d) is list:
            d = d[int(k)]
        elif k not in d:
            d[k] = {}
        else:
            d = d[k]
    return d


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) in [list, tuple] else [data]
