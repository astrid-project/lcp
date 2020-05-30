from jproperties import Properties


def property_parser(type, schema, source, path, value):
    with open(source, 'rb') as file:
        content = Properties()
        content.load(file, 'utf-8')
        k = '.'.join(path)
        old_value, _ = content[k]
        if old_value != value:
            content[k] = value
            with open(source, 'wb') as file:
                content.store(file, encoding='utf-8')
                return dict(type=type, schema=schema, source=source, path=path,
                            value=dict(new=value, old=old_value))
        else:
            return dict(type=type, schema=schema, source=source,
                        path=path, value=value, note='No change needed')
