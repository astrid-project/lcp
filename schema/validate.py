from falcon.errors import HTTPBadRequest
from marshmallow.exceptions import ValidationError
from utils.sequence import is_list


def _in(call):
    return lambda field: field in call()


def _not_in(call):
    return lambda field: field not in call()


def unique_list(field = None):
    def __get(values):
        if field is not None:
            fields = [value.get(field, None) for value in values]
        else:
            fields = values
        return len(fields) == len(set(fields))
    return __get


def validate(schema, method, data, check_unique_id=False, id=None):
    setattr(schema, 'method', method)
    try:
        if id is not None:
            if is_list(data):
                raise ValidationError(dict(id=msg_only_one_record))
            elif id in data:
                raise ValidationError(dict(id=msg_present_in_request_uri))
            else:
                data.update(id=id)
        if check_unique_id and is_list(data) and not unique_list('id')(data):
            raise ValidationError(dict(id=[msg_id_multiple_times]))
        schema.load(data)
    except ValidationError as val_err:
        raise HTTPBadRequest(title='Error', description=val_err.normalized_messages())
    return data


msg_repeated_values = 'Repeated values.'
msg_id_already_found = 'Id already found.'
msg_id_multiple_times = 'Same id present multiple times in the request.'
msg_id_not_found = 'Id not found.'
msg_id_not_in_catalog = 'Id not present in the catalog.'
msg_id_unique = 'Id must be unique.'
msg_only_one_record = 'When the id is present in the request uri only one record can be managed.'
msg_present_in_request_uri = 'Present in the request uri.'
msg_readonly = 'Readonly field.'
