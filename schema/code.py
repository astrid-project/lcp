from marshmallow import Schema
from marshmallow.fields import Bool, DateTime, Nested, Str
from utils.datetime import FORMAT


class CodeRequestSchema(Schema):
    """Request for code endpoint."""

    name = Str(required=True, example='firewall',
               description='Code name.')

    source = Str(required=True,
                 description='Code source')


class CodeResultResponseSchema(Schema):
    """Single item of the code results."""

    warning = Str(example='Useless properties: id',
                  description='Warning message.')


class CodeInjectedResponseSchema(CodeResultResponseSchema):
    """Single item of the code inject response."""

    name = Str(required=True, example='firewall',
               description='Code name')

    injected = Bool(required=True, example=True,
                    description='Indicate if the code was injected.')


class CodeErrorResponseSchema(CodeResultResponseSchema):
    """Error related to a single item of code response."""

    error = Bool(required=True, default=False, example=True,
                 description='Indicate the presence of an error.')

    description = Str(required=True, example='Missing name.',
                      description='Human readable message that describes the error.')


class CodeResponseSchema(Schema):
    """Response for code endpoint."""

    when = DateTime(format=FORMAT, required=True, example='2020/02/13 15:27:06',
                    description='Datetime of the configuration changes.')

    results = Nested(CodeResultResponseSchema, many=True, required=True)
