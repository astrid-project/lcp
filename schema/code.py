from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str
from schema.base import Base_Schema
from utils.datetime import FORMAT

__all__ = [
    'Code_Request_Schema',
    'Code_Response_Schema'
]


class Code_Request_Schema(Base_Schema):
    """Request for code endpoint."""

    name = Str(required=True, example='firewall',
               description='Code name.')
    source = Str(required=True,
                 description='Code source')


class Code_Result_Response_Schema(Base_Schema):
    """Single item of the code results."""

    warning = Str(example='Useless properties: id',
                  description='Warning message.')


class Code_Injected_Response_Schema(Code_Result_Response_Schema):
    """Single item of the code inject response."""

    name = Str(required=True, example='firewall',
               description='Code name')
    injected = Bool(required=True, example=True,
                    description='Indicate if the code was injected.')


class Code_Error_Response_Schema(Code_Result_Response_Schema):
    """Error related to a single item of code response."""

    error = Bool(required=True, default=False, example=True,
                 description='Indicate the presence of an error.')
    description = Str(required=True, example='Missing name.',
                      description='Human readable message that describes the error.')


class Code_Response_Schema(Base_Schema):
    """Response for code endpoint."""

    when = Date_Time(format=FORMAT, required=True, example='2020/02/13 15:27:06',
                     description='Datetime of the configuration changes.')
    results = Nested(Code_Result_Response_Schema, many=True, required=True)
