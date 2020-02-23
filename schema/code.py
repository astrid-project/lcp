from marshmallow import fields, Schema


class CodeRequestSchema(Schema):
    """
    Request for code endpoint.
    """
    name = fields.String(required=True, description='Code name.', example='firewall')
    source = fields.String(required=True, description='Code source')


class CodeResultResponseSchema(Schema):
    """
    Single item of the code results.
    """
    warning = fields.String(description='Warning message.', example='Useless properties: id')


class CodeInjectedResponseSchema(CodeResultResponseSchema):
    """
    Single item of the code inject response.
    """
    name = fields.String(required=True, description='Code name', example='firewall')
    injected = fields.Boolean(required=True, description='Indicate if the code was injected.', example=True)

class CodeErrorResponseSchema(CodeResultResponseSchema):
    """
    Error related to a single item of code response.
    """
    error = fields.Boolean(required=True, enum=[True], description='Indicate the presence of an error.', example=True)
    description = fields.String(required=True, description='Human readable message that describes the error.',
                                example='Missing name')


class CodeResponseSchema(Schema):
    """
    Response for code endpoint.
    """
    when = fields.DateTime(required=True, description='Datetime of the configuration changes.', example='2020/02/13-15:27:06')
    results = fields.Nested(CodeResultResponseSchema, many=True, required=True)
