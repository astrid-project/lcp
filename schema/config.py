from marshmallow import fields, Schema

class ActionRequestSchema(Schema):
    cmd = fields.String(required=True)
    args = fields.List(fields.String())


class ParameterRequestSchema(Schema):
    destination = fields.String(required=True)
    name = fields.String(required=True)
    sep = fields.String(required=True)
    value = fields.String(required=True)


class ResourceRequestSchema(Schema):
    destination = fields.String(required=True)
    content = fields.String(required=True)

class ConfigRequestSchema(Schema):
    actions = fields.List(fields.Nested(ActionRequestSchema()))
    parameters = fields.List(fields.Nested(ParameterRequestSchema()))
    resources = fields.List(fields.Nested(ResourceRequestSchema()))

class ResultResponseSchema(Schema):
    type = fields.String(required=True)
    warning = fields.String()


class ErrorResponseSchema(ResultResponseSchema):
    error = fields.Boolean(required=True)
    description = fields.String(required=True)


class ActionResponseSchema(ResultResponseSchema):
    execute = fields.String(required=True)
    stdout = fields.String()
    stderr = fields.String()
    return_code = fields.Integer(data_key='return-code', required=True)


class ParameterResponseSchema(ResultResponseSchema):
    destination = fields.String(required=True)
    name = fields.String(required=True)
    value = fields.String(required=True)


class ResourceResponseSchema(ResultResponseSchema):
    destination = fields.String(required=True)


class ConfigResponseSchema(Schema):
    when = fields.DateTime(required=True)
    results = fields.List(fields.Nested(ResultResponseSchema()), required=True)
