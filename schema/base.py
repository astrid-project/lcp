from lib.http import HTTP_Method
from lib.response import *
from marshmallow import Schema, validates_schema
from marshmallow.exceptions import ValidationError as Validation_Error
from utils.sequence import is_dict, is_list

__all__ = [
    'Base_Schema'
]


class Base_Schema(Schema):
    def __init__(self, *args, method=None, check_unique_id=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = method
        self.check_unique_id = check_unique_id

    def validate(self, data):
        try:
            self.load(data)
            return Ok_Response(data), True
        except Validation_Error as val_err:
            def __norm(block):
                for field in block.keys():
                    if is_list(block[field]):
                        block[field] = block[field].pop()
                    elif is_dict(block[field]):
                        __norm(block[field])
                return block
            msg = __norm(val_err.normalized_messages())
            return Not_Acceptable_Response(msg), False

    @validates_schema(skip_on_field_errors=False)
    def __validate_readonly(self, data, **kwargs):
        if self.method == HTTP_Method.PUT:
            for field, props in self.declared_fields.items():
                if props.metadata.get('readonly', False) and data.get(field, None) is not None:
                    msg = 'Readonly field.'
                    raise Validation_Error({field: msg})
