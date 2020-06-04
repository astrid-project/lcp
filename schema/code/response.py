from marshmallow import Schema
from marshmallow.fields import Bool, Constant, DateTime, Nested, Str


class CodeResultResponseSchema(Schema):
    """Single item of the code results."""
    warning = Str(description='Warning message.',
                  example='Useless properties: id')


class CodeInjectedResponseSchema(CodeResultResponseSchema):
    """Single item of the code inject response."""
    name = Str(required=True, description='Code name', example='firewall')
    injected = Bool(required=True, example=True,
                    description='Indicate if the code was injected.')


class CodeErrorResponseSchema(CodeResultResponseSchema):
    """Error related to a single item of code response."""
    error = Constant(required=True, constant=True,
                     description='Indicate the presence of an error.')
    description = Str(required=True, description='Human readable message that describes the error.',
                      example='Missing name.')


class CodeResponseSchema(Schema):
    """Response for code endpoint."""
    when = DateTime(required=True, description='Datetime of the configuration changes.',
                    example='2020/02/13 15:27:06')
    results = Nested(CodeResultResponseSchema, many=True, required=True)
