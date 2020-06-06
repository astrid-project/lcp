from resource.config.parameters.json_parser import json_parser
from resource.config.parameters.yaml_parser import yaml_parser
from resource.config.parameters.property_parser import property_parser
from os.path import expanduser
from utils.data import get_none
from utils.sequence import exclude_keys, wrap


def make_parameters(self, data):
    type = 'parameter'
    schema = data.get('schema', None)
    source = data.get('source', None)
    path = data.get('path', None)
    value = data.get('value', None)
    missing_values = get_none(
        schema=schema, source=source, path=path, value=value)
    if len(missing_values) > 0:
        output = dict(type=type, error=True,
                      description=f'Missing {",".join(missing_values)}')
    elif schema not in ['yaml', 'json', 'properties']:
        output = dict(type=type, error=True,
                      description=f'Schema {schema} not valid. Must be one of yaml, json or properties')
    else:
        path = wrap(path)
        try:
            source = expanduser(source)
            if schema == 'yaml':
                output = yaml_parser(type, schema, source, path, value)
            elif schema == 'json':
                output = json_parser(type, schema, source, path, value)
            elif schema == 'properties':
                output = property_parser(type, schema, source, path, value)
        except FileNotFoundError as file_not_found_error:
            self.log.error(f'Exception: {file_not_found_error}')
            output = dict(error=True, type=type, data=data,
                          description=f'Source {source} not found',
                          exception=str(file_not_found_error))
        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            output = dict(error=True, type=type, data=data,
                          description=f'Source {source} not accessible',
                          exception=str(exception))
    useless_properties = exclude_keys(
        data, 'schema', 'source', 'path', 'value')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
