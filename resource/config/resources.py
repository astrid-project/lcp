from os.path import expanduser
from utils.data import get_none
from utils.sequence import exclude_keys

def make_resources(self, data):
    type = 'resource'
    dest = data.get('destination', None)
    content = data.get('content', None)
    missing_values = get_none(destination=dest, content=content)
    if len(missing_values) > 0:
        output = dict(type=type, error=True, description=f'Missing {",".join(missing_values)}')
    else:
        try:
            fix_dest = expanduser(dest)
            with open(fix_dest, "w") as file:
                file.write(content)
                output = dict(type=type, destination=dest)
        except FileNotFoundError as file_not_found_error:
            self.log.error(f'Exception: {file_not_found_error}')
            output = dict(type=type, error=True, description=f'Destination {dest} not found')
        except Exception as exception:
            self.log.error(f'Exception {exception}')
            output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
    useless_properties = exclude_keys(data, 'destination', 'content')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
