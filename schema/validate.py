__all__ = [
    'In',
    'Unique_List'
]


class In(object):
    error_messages = dict(validator_failed='Id not found.')

    @staticmethod
    def apply(src, negation=False):
        def data():
            return src() if callable(src) else src
        if negation:
            return lambda field: field not in data()
        else:
            return lambda field: field in data()


class Unique_List(object):
    error_messages = dict(validator_failed='Repeated values.')

    @staticmethod
    def apply(field=None):
        def __get(values):
            if field is not None:
                fields = [value.get(field, None) for value in values]
            else:
                fields = values
            return len(fields) == len(set(fields))
        return __get
