from utils.sequence import exclude_keys

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


def get_data(data, *keys):
    res = {}
    for d in data:
        v = data.get(d, None)
        if v is None:
            res[d] = v
    output = dict(error=True, description=f'Missing {get_none(**res)}')
    useless_properties = exclude_keys(data, *keys)
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return res.values + [output]
