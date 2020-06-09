from jproperties import Properties
from utils.log import Log
from utils.sequence import iterate

import json
import yaml


def json_parser(schema, source, path, value):
    with open(source, 'r') as file:
        content = json.load(file)
        d = iterate(content, *path[:-1])
        old_value = d[path[-1]]
        if old_value != value:
            d[path[-1]] = value
            with open(source, 'w') as file:
                json.dump(content, file, sort_keys=True, indent=3)
                return dict(schema=schema, source=source, path=path, value=dict(new=value, old=old_value))
        else:
            return dict(schema=schema, source=source, path=path, value=value, note='No change needed')


def property_parser(schema, source, path, value):
    with open(source, 'rb') as file:
        content = Properties()
        content.load(file, 'utf-8')
        k = '.'.join(path)
        try:
            old_value, _ = content[k]
        except Exception as exception:
            Log.get('property-parser').error(f'exception: {exception}')
            old_value = None
        if old_value != value:
            content[k] = value
            with open(source, 'wb') as file:
                content.store(file, encoding='utf-8')
                return dict(schema=schema, source=source, path=path, value=dict(new=value, old=old_value))
        else:
            return dict(schema=schema, source=source, path=path, value=value, note='No change needed')


def yaml_parser(schema, source, path, value):
    with open(source, "r") as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
        d = iterate(content, *path[:-1])
        old_value = d[path[-1]]
        if old_value != value:
            d[path[-1]] = value
            with open(source, 'w') as file:
                yaml.dump(content, file, sort_keys=True, indent=3)
                return dict(schema=schema, source=source, path=path, value=dict(new=value, old=old_value))
        else:
            return dict(schema=schema, source=source, path=path, value=value, note='No change needed')
