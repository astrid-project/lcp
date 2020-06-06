from os.path import expanduser
from utils.data import get_none
from utils.sequence import exclude_keys

def make_resources(self, data):
    type = 'resource'
    path = data.get('path', None)
    content = data.get('content', None)
    missing_values = get_none(path=path, content=content)
    if len(missing_values) > 0:
        output = dict(type=type, error=True, description=f'Missing {",".join(missing_values)}')
    else:
        try:
            fix_path = expanduser(path)
            with open(fix_dest, "w") as file:
                file.write(content)
                output = dict(type=type, path=path)
        except FileNotFoundError as file_not_found_error:
            self.log.error(f'Exception: {file_not_found_error}')
            output = dict(type=type, error=True, description=f'Path [path] not found', data=data)
        except Exception as exception:
            self.log.error(f'Exception {exception}')
            output = dict(type=type, error=True, description=f'Path [path] not accessible', data=data)
    useless_properties = exclude_keys(data, 'path', 'content')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
