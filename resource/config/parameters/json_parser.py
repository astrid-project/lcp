from utils.sequence import iterate

import json


def json_parser(type, schema, source, path, value):
    with open(source, 'r') as file:
        content = json.load(file)
        d = iterate(content, *path[:-1])
        old_value = d[path[-1]]
        if old_value != value:
            d[path[-1]] = value
            with open(source, 'w') as file:
                json.dump(content, file, sort_keys=True, indent=3)
                return dict(type=type, schema=schema, source=source, path=path,
                            value=dict(new=value, old=old_value))
        else:
            return dict(type=type, schema=schema, source=source,
                        path=path, value=value, note='No change needed')
