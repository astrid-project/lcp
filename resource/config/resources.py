def make_resources(self, data):
    type = 'resource'
    dest = data.get('destination', None)
    content = data.get('content', None)
    if dest is None or content is None:
        output = dict(type=type, error=True,
                        description=f'Missing {get_none(destination=dest, content=content)}')
    else:
        try:
            fix_dest = os.path.expanduser(dest)
            with open(fix_dest, "w") as file:
                file.write(content)
                output = dict(type=type, destination=dest)
        except FileNotFoundError as file_not_found_error:
            self.log.debug(file_not_found_error)
            output = dict(
                type=type, error=True, description=f'Destination {dest} not found')
        except Exception as e:
            self.log.debug(e)
            output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
    useless_properties = exclude_keys(data, 'destination', 'content')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
