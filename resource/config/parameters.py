def make_parameters(self, data):
    type = 'parameter'
    schema = data.get('schema', None)
    source = data.get('source', None)
    path = data.get('path', None)
    value = data.get('value', None)
    if schema is None or source is None or path is None or value is None:
        output = dict(type=type, error=True,
                      description=f'Missing {get_none(schema=schema, source=source, path=path, value=value)}')
    elif schema not in ['yaml', 'json', 'properties']:
        output = dict(type=type, error=True,
                      description=f'Schema {schema} not valid. Must be one of yaml, json or properties')
    else:
        path = wrap(path)
        try:
            source = os.path.expanduser(source)
            if schema == 'yaml':
                with open(source, "r") as file:
                    content = yaml.load(file, Loader=yaml.FullLoader)
                    d = iterate(content, *path[:-1])
                    old_value = d[path[-1]]
                    if old_value != value:
                        d[path[-1]] = value
                        with open(source, 'w') as file:
                            yaml.dump(content, file,
                                        sort_keys=True, indent=3)
                            output = dict(type=type, schema=schema, source=source, path=path, value={
                                                'new': value, 'old': old_value})
                    else:
                        output = dict(type=type, schema=schema, source=source,
                                        path=path, value=value, note='No change needed')
            elif schema == 'json':
                with open(source, 'r') as file:
                    content = json_lib.load(file)
                    d = iterate(content, *path[:-1])
                    old_value = d[path[-1]]
                    if old_value != value:
                        d[path[-1]] = value
                        with open(source, 'w') as file:
                            json_lib.dump(
                                content, file, sort_keys=True, indent=3)
                            output = dict(type=type, schema=schema, source=source, path=path, value={
                                            'new': value, 'old': old_value})

                    else:
                        output = dict(type=type, schema=schema, source=source,
                                        path=path, value=value, note='No change needed')
            elif schema == 'properties':
                with open(source, 'rb') as file:
                    content = Properties()
                    content.load(file, 'utf-8')
                    k = '.'.join(path)
                    old_value, _ = content[k]
                    if old_value != value:
                        content[k] = value
                        with open(source, 'wb') as file:
                            content.store(file, encoding='utf-8')
                            output = dict(type=type, schema=schema, source=source, path=path, value={
                                            'new': value, 'old': old_value})
                    else:
                        output = dict(type=type, schema=schema, source=source,
                                        path=path, value=value, note='No change needed')
        except FileNotFoundError as file_not_found_error:
            self.log.debug(file_not_found_error)
            output = dict(
                type=type, error=True, description=f'Source {source} not found')
        except Exception as e:
            self.log.debug(e)
            output = dict(type=type, error=True,
                            description=f'Source {source} not accessible')
    useless_properties = exclude_keys(data, 'schema', 'source', 'path', 'value')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
