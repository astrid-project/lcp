from utils.sequence import exclude_keys


def get_none(**vars):
    """ Get the keys that are None value.

    :param vars: key/value arguments
    :returns: keys with value = None
    """
    res = []
    for text, var in vars.items():
        if var is None:
            res.append(text)
    return res


def get_data(data, *keys):
    res = {}
    for k in keys:
        v = data.get(k, None)
        res[k] = v

    output = {}
    none_vals = get_none(**res)
    if len(none_vals) > 0:
        output = dict(error=True, description=f'Missing {".".join(none_vals)}')

    useless_properties = exclude_keys(data, *keys)
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'

    return list(res.values()) + [output]
