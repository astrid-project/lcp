import json
import os

import dpath.util
import xmltodict as xml_to_dict
import yaml
from jproperties import Properties
from yaml import FullLoader as Full_Loader

from utils.log import Log

NO_CHANGE_NEEDED = 'No change needed'


def json_parser(schema, source, path, value):
    if os.stat(source).st_size == 0:
        content = {}
    else:
        with open(source, 'r') as file:
            content = json.load(file)
    old_value = dpath.util.get(content, path, default=None)
    if old_value != value:
        if old_value is None:
            dpath.util.new(content, path, value)
        else:
            dpath.util.set(content, path, value)
        with open(source, 'w') as file:
            json.dump(content, file, sort_keys=True, indent=3)
            return {'value': {'new': value, 'old': old_value}}
    else:
        return {'note': NO_CHANGE_NEEDED}


def xml_parser(schema, source, path, value):
    if os.stat(source).st_size == 0:
        content = {}
    else:
        with open(source, "r") as file:
            content = xml_to_dict.parse(file.read())
    old_value = dpath.util.get(content, path, default=None)
    if old_value != value:
        if old_value is None:
            dpath.util.new(content, path, value)
        else:
            dpath.util.set(content, path, value)
        with open(source, 'w') as file:
            xml_to_dict.unparse(content, output=file, pretty=True)
            return {'value': {'new': value, 'old': old_value}}
    else:
        return {'note': NO_CHANGE_NEEDED}


def yaml_parser(schema, source, path, value):
    if os.stat(source).st_size == 0:
        content = {}
    else:
        with open(source, "r") as file:
            content = yaml.load(file, Loader=Full_Loader)
    old_value = dpath.util.get(content, path, default=None)
    if old_value != value:
        if old_value is None:
            dpath.util.new(content, path, value)
        else:
            dpath.util.set(content, path, value)
        with open(source, 'w') as file:
            yaml.dump(content, file, sort_keys=True, indent=3)
            return {'value': {'new': value, 'old': old_value}}
    else:
        return{'note': NO_CHANGE_NEEDED}


def property_parser(schema, source, path, value):
    with open(source, 'rb') as file:
        content = Properties()
        content.load(file, 'utf-8')
        k = '.'.join(path)
        try:
            old_value, _ = content[k]
        except Exception as e:
            Log.get('property-parser').exception(f'Parsing property {k}', e)
            old_value = None
        if old_value != value:
            content[k] = value
            with open(source, 'wb') as file:
                content.store(file, encoding='utf-8')
                return {'value': {'new': value, 'old': old_value}}
        else:
            return {'note': NO_CHANGE_NEEDED}
